from flask import request, jsonify, Blueprint
from src.config import app
from src.logger import logger
from src.alerts import slack_alert, send_smtp_email
from src.models import NotificationSettings
from src.routes.helper.common_helper import get_email_addresses

alert_bp = Blueprint('alert', __name__)

@app.route('/alerts', methods=['POST'])
def receive_alerts():
    """
    Endpoint to receive alerts from an external source.

    This function validates the incoming request, processes alert data,
    logs the alerts based on severity, and sends notifications via Slack
    and email.

    Returns:
        JSON response indicating the status of the request:
        - 200 if alerts are processed successfully
        - 400 if no alert data is received
        - 415 if the Content-Type is not application/json
        - 500 if an internal error occurs
    """
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type: Expected application/json"}), 415

    try:
        alert_data = request.json
        if not alert_data or 'alerts' not in alert_data:
            return jsonify({"error": "No alert data received"}), 400

        for alert in alert_data['alerts']:
            handle_alert(alert)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.exception("Error processing alert")  # Log the full exception for debugging
        return jsonify({"error": "An error occurred while processing the alert"}), 500


def handle_alert(alert):
    """
    Processes a single alert.

    This function extracts relevant information from the alert and
    triggers logging and notification functions.

    Args:
        alert (dict): The alert data containing labels and annotations.
    """
    alert_name = alert['labels'].get('alertname', 'Unknown Alert')
    instance = alert['labels'].get('instance', 'Unknown Instance')
    severity = alert['labels'].get('severity', 'info')
    description = alert['annotations'].get('description', 'No description provided')
    summary = alert['annotations'].get('summary', 'No summary provided')

    log_alert(severity, alert_name, instance, description, summary)
    send_alert_notifications(alert_name, instance, severity, description, summary)


def log_alert(severity, alert_name, instance, description, summary):
    """
    Logs the received alert based on its severity.

    This function records the alert information using the appropriate log level.

    Args:
        severity (str): The severity level of the alert (e.g., critical, warning, info).
        alert_name (str): The name of the alert.
        instance (str): The instance associated with the alert.
        description (str): A detailed description of the alert.
        summary (str): A brief summary of the alert.
    """
    message = f"Alert received: {alert_name} - {instance} - {severity} - {description} - {summary}"
    if severity == 'critical':
        logger.error(message)
    elif severity == 'warning':
        logger.warning(message)
    else:
        logger.info(message)


def send_alert_notifications(alert_name, instance, severity, description, summary):
    """
    Sends notifications for the received alert.

    This function sends a Slack alert and an email notification to admin users.

    Args:
        alert_name (str): The name of the alert.
        instance (str): The instance associated with the alert.
        severity (str): The severity level of the alert.
        description (str): A detailed description of the alert.
        summary (str): A brief summary of the alert.
    """
    slack_webhook_url = NotificationSettings.get_slack_webhook_url()
    slack_alert.send_slack_alert(
        slack_webhook_url,
        message=summary,
        title=alert_name,
        fields=[
            {"title": "Instance", "value": instance, "short": True},
            {"title": "Severity", "value": severity, "short": True},
            {"title": "Description", "value": description, "short": False}
        ]
    )

    admin_emails = get_email_addresses(user_level="admin", receive_email_alerts=True)
    send_smtp_email(
        receiver_email=admin_emails,
        subject=f"{alert_name} Alert",
        body=f"{summary}\n\n{description}",
        is_html=False,
        bypass_alerts=False
    )
