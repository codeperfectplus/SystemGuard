import json
import requests
from datetime import datetime

def send_slack_alert(webhook_url, message, title="System Alert", color="#36a64f", fields=None, username="System Metrics Bot", icon_emoji=":robot_face:"):
    """
    Sends a formatted notification message to a Slack channel via webhook.
    
    Parameters:
    webhook_url (str): The Slack incoming webhook URL.
    message (str): The main message content.
    title (str): Title of the message.
    color (str): Color of the message attachment.
    fields (list of dict): Optional. Extra information fields to include.
    username (str): Username of the bot sending the message.
    icon_emoji (str): Emoji icon to show in Slack.
    """

    # Build the payload
    payload = {
        "username": username,
        "icon_emoji": icon_emoji,
        "attachments": [
            {
                "fallback": title,
                "color": color,
                "title": title,
                "text": message,
                "fields": fields if fields else [],
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
    
    print(f"Notification sent to Slack: {title}")

# Example usage
# webhook_url = ''
# message = "High CPU usage detected. Usage is above 85%."
# fields = [
#     {"title": "Metric", "value": "CPU Usage", "short": True},
#     {"title": "Threshold", "value": "85%", "short": True},
#     {"title": "Current Usage", "value": "92%", "short": True}
# ]

# send_slack_notification(
#     webhook_url,
#     message=message,
#     title="High CPU Usage Alert",
#     color="#ff0000",
#     fields=fields
# )
