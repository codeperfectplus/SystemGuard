import json
import requests
from datetime import datetime
from src.logger import logger

def send_slack_alert(webhook_url, alert_name, instance, severity, description, summary):
    """
    Sends a formatted notification message to a Slack channel via webhook.
    
    Parameters:
    webhook_url (str): The Slack incoming webhook URL.
    alert_name (str): The name of the alert.
    instance (str): The instance related to the alert.
    severity (str): The severity level of the alert.
    description (str): A detailed description of the alert.
    summary (str): Summary of the alert. Default is "Prometheus Alert".
    color (str): Color of the message attachment.
    username (str): Username of the bot sending the message.
    icon_emoji (str): Emoji icon to show in Slack.
    """

    # Build the payload
    color_dict = {
        "critical": "#ee1b1b", # Red
        "warning": "#eeee1b", # Yellow
        "info": "#16d119" # Green
    }
    
    payload = {
        "username": "SystemGuard Alert",
        "attachments": [
            {
                "fallback": alert_name,
                "color": color_dict.get(severity, "gray"),
                "title": alert_name,
                "text": summary,
                "fields": [
                    {"title": "Instance", "value": instance, "short": True},
                    {"title": "Severity", "value": severity, "short": True},
                    {"title": "Description", "value": description, "short": False},
                ],
                "footer": "System Metrics",
                "ts": f"{datetime.now().timestamp()} UTC"
            }
        ]
    }
    
    # Send the POST request to the Slack webhook URL
    response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    
    # Check the response status
    if response.status_code != 200:
        raise Exception(f"Request to Slack failed with status code {response.status_code}, response: {response.text}")
    
    logger.info(f"Alert sent to Slack: {alert_name}") 
