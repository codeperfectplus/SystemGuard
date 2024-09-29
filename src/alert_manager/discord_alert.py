from datetime import datetime
import requests
from src.logger import logger

def send_discord_alert(webhook_url, alert_name, instance, severity, description, summary):
    """
    Sends an alert to a Discord channel via a webhook.

    Args:
        webhook_url (str): The webhook URL for the Discord channel.
        alert_name (str): The name of the alert.
        instance (str): The instance associated with the alert.
        severity (str): The severity level of the alert (e.g., critical, warning, info).
        description (str): A detailed description of the alert.
        summary (str): A brief summary of the alert.

    Returns:
        bool: True if the alert was sent successfully, False otherwise.
    """
    
    # Constructing the message to send to Discord
    color_dict = {
        "critical": 16711680,  # Red
        "warning": 16776960,  # Yellow
        "info": 65280  # Green
    }
    message = {
        "embeds": [
            {
                "title": f"🚨 **{alert_name}** 🚨",
                "color": color_dict.get(severity, 0),
                "fields": [
                    {"name": "Instance", "value": instance, "inline": True},
                    {"name": "Severity", "value": severity, "inline": True},
                    {"name": "Description", "value": description, "inline": False},
                    {"name": "Summary", "value": summary, "inline": False}
                ],
                "footer": {
                    "text": "System Guard Alert"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    }
    
    # Send the POST request to the Discord webhook URL
    response = requests.post(webhook_url, json=message)

    # Check the response status
    if response.status_code != 204:
        logger.error(f"Failed to send alert to Discord: {response.status_code}, {response.text}")
        return False

    logger.info(f"Alert sent to Discord: {alert_name}")
    return True
