import os
from flask import request, jsonify, Blueprint
from src.config import app
from src.logger import logger
from src.alert_manager import (
    send_slack_alert,
    send_smtp_email,
    send_discord_alert,
    send_teams_alert,
    send_google_chat_alert,
)
from src.models import NotificationSettings
from src.routes.helper.common_helper import get_email_addresses
from src.routes.helper.notification_helper import send_test_alert
from src.utils import get_ip_address, render_template_from_file, ROOT_DIR

alert_bp = Blueprint("alert", __name__)


@app.route("/alerts", methods=["POST"])
def receive_alerts():
    """
    Receives and processes incoming alerts from external sources.

    Validates the request content type and alert data, logs the alert based on severity,
    and triggers notifications via Slack, email, and Discord.

    Returns:
        JSON response indicating the result of alert processing:
        - 200 if successfully processed
        - 400 if alert data is missing
        - 415 if the content type is not application/json
        - 500 if an internal server error occurs
    """
    if request.headers.get("Content-Type") != "application/json":
        return (
            jsonify({"error": "Unsupported Media Type. Expected application/json"}),
            415,
        )

    try:
        alert_data = request.json
        if not alert_data or "alerts" not in alert_data:
            return jsonify({"error": "No alert data received"}), 400

        for alert in alert_data["alerts"]:
            process_alert(alert)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.exception("Error occurred while processing alert")
        return (
            jsonify({"error": "An internal error occurred while processing the alert"}),
            500,
        )


def process_alert(alert):
    """
    Handles an individual alert by extracting necessary details and
    triggering logging and notification mechanisms.

    Args:
        alert (dict): The alert payload containing labels and annotations.
    """
    alert_name = alert["labels"].get("alertname", "Unknown Alert")
    instance = alert["labels"].get("instance", "Unknown Instance")
    severity = alert["labels"].get("severity", "info")
    description = alert["annotations"].get("description", "No description provided")
    summary = alert["annotations"].get("summary", "No summary provided")

    log_alert(severity, alert_name, instance, description, summary)
    notify_alert(alert_name, instance, severity, description, summary)


def log_alert(severity, alert_name, instance, description, summary):
    """
    Logs the alert message with the appropriate log level based on its severity.

    Args:
        severity (str): Severity level of the alert (e.g., critical, warning, info).
        alert_name (str): Name of the alert.
        instance (str): Instance generating the alert.
        description (str): Detailed alert description.
        summary (str): Brief alert summary.
    """
    message = f"Alert: {alert_name} - Instance: {instance} - Severity: {severity} - {summary} - {description}"

    log_method = {
        "critical": logger.error,
        "warning": logger.warning,
        "info": logger.info,
        "debug": logger.debug,
    }.get(severity, logger.info)
    log_method(message)


@app.route("/alerts/test", methods=["GET"])
def test_alert():
    alertmanager_ip = get_ip_address()
    alertmanager_port = "9093"
    alertmanager_url = f"http://{alertmanager_ip}:{alertmanager_port}"

    # Send a test alert with a unique name
    response = send_test_alert(alertmanager_url, "Test Alert", "info", "Test Instance")
    return jsonify(response), response.get("status", 500)



def get_notification_settings():
    """
    Retrieves the notification settings from the database.

    Returns:
        dict: Dictionary of notification settings.
    """
    return NotificationSettings().to_dict()

def is_enabled(notification_config, setting_key):
    """
    Checks if a particular notification setting is enabled.

    Args:
        notification_config (dict): Notification settings configuration.
        setting_key (str): The key corresponding to the setting.
    
    Returns:
        bool: True if the setting is enabled, False otherwise.
    """
    return notification_config.get(setting_key, False)

def send_slack_alert_wrapper(config, alert_name, instance, severity, description, summary):
    """
    Sends a Slack alert using the provided configuration.

    Args:
        config (dict): Notification configuration.
        alert_name (str), instance (str), severity (str), description (str), summary (str)
    """
    slack_webhook = config.get("slack_webhook_url")
    if slack_webhook:
        send_slack_alert(slack_webhook, alert_name, instance, severity, description, summary)
          

def send_email_alert_wrapper(alert_name, instance, severity, description, summary):
    """
    Sends email alerts to administrators.

    Args:
        alert_name (str), description (str), summary (str)
    """
    admin_emails = get_email_addresses(user_level="admin", receive_email_alerts=True)
    logger.info(f"Sending email alert to {admin_emails}")
    context = {
        "alert_name": alert_name,
        "instance": instance,
        "severity": severity,
        "description": description,
        "summary": summary, 
    }

    login_alert_template = os.path.join(
        ROOT_DIR, "src/templates/email_templates/alert_template.html"
    )
    email_body = render_template_from_file(
        login_alert_template, **context
    )
    if admin_emails:
        send_smtp_email(
            receiver_email=admin_emails,
            subject=f"{alert_name} Alert",
            body=email_body,
            is_html=True,
        )


def send_discord_alert_wrapper(config, alert_name, instance, severity, description, summary):
    """
    Sends a Discord alert using the provided configuration.
    """
    discord_webhook = config.get("discord_webhook_url")
    if discord_webhook:
        send_discord_alert(
            discord_webhook, alert_name, instance, severity, description, summary
        )


def send_teams_alert_wrapper(config, alert_name, instance, severity, description, summary):
    """
    Sends a Microsoft Teams alert using the provided configuration.
    """
    teams_webhook_url = config.get("teams_webhook_url")
    if teams_webhook_url:
        send_teams_alert(
            teams_webhook_url, alert_name, instance, severity, description, summary
        )
   
def send_google_chat_alert_wrapper(config, alert_name, instance, severity, description, summary):
    """
    Sends a Google Chat alert using the provided configuration.
    """

    google_chat_webhook_url = config.get("google_chat_webhook_url")
    if google_chat_webhook_url:
        send_google_chat_alert(
            google_chat_webhook_url, alert_name, instance, severity, description, summary
        )


def notify_alert(alert_name, instance, severity, description, summary):
    """
    Sends notifications for the alert via Slack, email, and Discord.

    Args:
        alert_name (str): Name of the alert.
        instance (str): Instance associated with the alert.
        severity (str): Severity level of the alert.
        description (str): Detailed description of the alert.
        summary (str): Brief summary of the alert.
    """
    notification_config = get_notification_settings()

    if is_enabled(notification_config, "is_email_alert_enabled"):
        send_email_alert_wrapper(alert_name, instance, severity, description, summary)

    if is_enabled(notification_config, "is_slack_alert_enabled"):
        send_slack_alert_wrapper(notification_config, alert_name, instance, severity, description, summary)

    if is_enabled(notification_config, "is_discord_alert_enabled"):
        send_discord_alert_wrapper(notification_config, alert_name, instance, severity, description, summary)

    if is_enabled(notification_config, "is_teams_alert_enabled"):
        send_teams_alert_wrapper(notification_config, alert_name, instance, severity, description, summary)

    if is_enabled(notification_config, "is_google_chat_alert_enabled"):
        send_google_chat_alert_wrapper(notification_config, alert_name, instance, severity, description, summary)
