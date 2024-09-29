import requests
import json
from src.logger import logger


def send_teams_alert(webhook_url, alert_name, instance, severity, description, summary="Prometheus Alert"):
    """
    Sends a Prometheus alert to a Microsoft Teams channel using a webhook.

    Parameters:
    webhook_url (str): The webhook URL of the Teams channel.
    alert_name (str): The name of the alert (e.g., CPU usage high).
    instance (str): The instance where the alert occurred (e.g., the hostname or IP).
    severity (str): The severity level of the alert (e.g., critical, warning).
    description (str): Detailed description of the alert.
    summary (str): A brief summary of the alert (default is 'Prometheus Alert').
    """

    # Define the message payload
    message_payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": summary,
        "themeColor": "FF0000" if severity.lower() == "critical" else "FFD700",  # Red for critical, Yellow for others
        "sections": [{
            "activityTitle": f"**Alert: {alert_name}**",
            "facts": [
                {"name": "Instance:", "value": instance},
                {"name": "Severity:", "value": severity},
                {"name": "Description:", "value": description}
            ],
            "text": description,
            "markdown": True
        }]
    }

    # Send the POST request to the webhook URL
    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(message_payload)
    )

    # Check if the request was successful
    if response.status_code == 200:
        logger.info(f"Alert sent successfully to Microsoft Teams! Alert: {alert_name}, Instance: {instance}, Severity: {severity}")
    else:
        logger.error(f"Failed to send alert. Status code: {response.status_code}")
        logger.error(f"Response: {response.text}")
