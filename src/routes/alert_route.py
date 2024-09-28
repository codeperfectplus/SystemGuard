from flask import request, jsonify, Blueprint
from src.config import app
from src.logger import logger
from src.alerts import slack_alert, send_smtp_email, send_alert_to_discord
from src.models import NotificationSettings
from src.routes.helper.common_helper import get_email_addresses

alert_bp = Blueprint('alert', __name__)

@app.route('/alerts', methods=['POST'])
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
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({"error": "Unsupported Media Type. Expected application/json"}), 415

    try:
        alert_data = request.json
        if not alert_data or 'alerts' not in alert_data:
            return jsonify({"error": "No alert data received"}), 400

        for alert in alert_data['alerts']:
            process_alert(alert)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.exception("Error occurred while processing alert")
        return jsonify({"error": "An internal error occurred while processing the alert"}), 500


def process_alert(alert):
    """
    Handles an individual alert by extracting necessary details and 
    triggering logging and notification mechanisms.

    Args:
        alert (dict): The alert payload containing labels and annotations.
    """
    alert_name = alert['labels'].get('alertname', 'Unknown Alert')
    instance = alert['labels'].get('instance', 'Unknown Instance')
    severity = alert['labels'].get('severity', 'info')
    description = alert['annotations'].get('description', 'No description provided')
    summary = alert['annotations'].get('summary', 'No summary provided')

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
        'critical': logger.error,
        'warning': logger.warning,
        'info': logger.info,
        'debug': logger.debug
    }.get(severity, logger.info)
    log_method(message)


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
    slack_webhook = NotificationSettings.get_slack_webhook_url()
    if slack_webhook:
        slack_alert.send_slack_alert(
            slack_webhook,
            title=alert_name,
            message=summary,
            fields=[
                {"title": "Instance", "value": instance, "short": True},
                {"title": "Severity", "value": severity, "short": True},
                {"title": "Description", "value": description, "short": False}
            ]
        )

    admin_emails = get_email_addresses(user_level="admin", receive_email_alerts=True)
    if admin_emails:
        send_smtp_email(
            receiver_email=admin_emails,
            subject=f"{alert_name} Alert",
            body=f"{summary}\n\n{description}",
            is_html=False
        )

    discord_webhook = NotificationSettings.get_discord_webhook_url()
    if discord_webhook:
        send_alert_to_discord(discord_webhook, alert_name, instance, severity, description, summary)
