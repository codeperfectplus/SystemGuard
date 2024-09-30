import os
import requests
import json
import time

from src.logger import logger
from src.alert_manager import (
    send_slack_alert,
    send_smtp_email,
    send_discord_alert,
    send_teams_alert,
    send_google_chat_alert,
)
from src.models import NotificationSettings, AlertDataModel
from src.routes.helper.common_helper import get_email_addresses
from src.utils import render_template_from_file, ROOT_DIR

# AlertDataModel
#     id = db.Column(db.Integer, primary_key=True)
#     alert_name = db.Column(db.String(255), nullable=False)
#     instance = db.Column(db.String(255), nullable=False)
#     severity = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.String(255), nullable=False)
#     summary = db.Column(db.String(255), nullable=False)


def send_test_alert(alertmanager_url, alert_name, severity, instance):
    # Generate a unique alert name by appending the current timestamp
    unique_alert_name = f"{alert_name}_{int(time.time())}"

    # Define the alert data with the unique alert name
    alert_data = [
        {
            "labels": {
                "alertname": unique_alert_name,
                "severity": severity,
                "instance": instance,
            },
            "annotations": {
                "description": f"This is a test alert generated at {time.strftime('%Y-%m-%d %H:%M:%S')}",
                "summary": "SystemGuards Test Alert Verification. Only for testing purposes. You can ignore this alert.",
            },
        }
    ]

    # Send the POST request to Alertmanager
    try:
        response = requests.post(
            f"{alertmanager_url}/api/v2/alerts",
            headers={"Content-Type": "application/json"},
            data=json.dumps(alert_data),
        )

        # Log response details
        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        # Check the response
        if response.status_code == 202 or response.status_code == 200:
            return {
                "message": f"Test alert '{unique_alert_name}' sent successfully!",
                "status": 200,
            }
        else:
            return {
                "message": f"Failed to send alert, Response: {response.text}",
                "status": response.status_code,
            }

    except Exception as e:
        return {"message": f"An error occurred: {e}", "status": 500}


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
    status = alert.get("status", "firing")
    start_time = alert.get("startsAt", "No start time provided")

    log_alert(severity, alert_name, instance, description, summary)
    notify_alert(alert_name, instance, severity, description, summary)
    save_alert_data(alert_name, instance, severity, description, summary, status, start_time)


def save_alert_data(alert_name, instance, severity, description, summary, status, start_time):
    """
    Saves the alert data to the database.

    Args:
        alert_name (str): Name of the alert.
        instance (str): Instance generating the alert.
        severity (str): Severity level of the alert.
        description (str): Detailed alert description.
        summary (str): Brief alert summary.
    """
    alert_data = AlertDataModel(
        alert_name=alert_name,
        instance=instance,
        severity=severity,
        description=description,
        summary=summary,
        status=status,
        start_time=start_time,
    )
    logger.info(f"Saving alert data: {alert_data}")
    alert_data.save()

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
    message = f"Alert: {alert_name}"

    log_method = {
        "critical": logger.error,
        "warning": logger.warning,
        "info": logger.info,
        "debug": logger.debug,
    }.get(severity, logger.info)
    log_method(message)


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
