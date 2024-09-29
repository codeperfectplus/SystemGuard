import requests
import json
from src.logger import logger

def send_google_chat_alert(webhook_url, alert_name, instance, severity, description, summary="Prometheus Alert"):
    """
    Sends an alert message to a Google Chat room using a webhook.

    Parameters:
    webhook_url (str): The webhook URL of the Google Chat room.
    alert_name (str): The name of the alert.
    instance (str): The instance (e.g., server or system) where the alert occurred.
    severity (str): The severity level of the alert (e.g., critical, warning).
    description (str): A description of the issue.
    summary (str): A summary or title of the message (defaults to 'Prometheus Alert').
    """
    # Define the message payload with card structure
    message_payload = {
        "cards": [
            {
                "header": {
                    "title": "SystemGuard Alert",
                    "subtitle": f"Alert: {alert_name}",
                    "imageUrl": "https://developers.google.com/chat/images/chat-product-icon.png",
                    "imageStyle": "IMAGE"
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "keyValue": {
                                    "topLabel": "Instance",
                                    "content": instance,
                                }
                            },
                            {
                                "keyValue": {
                                    "topLabel": "Severity",
                                    "content": severity,
                                }
                            },
                            {
                                "textParagraph": {
                                    "text": f"<b>Description:</b> {description}"
                                }
                            },
                            {
                                "textParagraph": {
                                    "text": f"<b>Summary:</b> {summary}"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Send the POST request to the webhook URL
    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(message_payload)
    )

    # Check if the request was successful
    if response.status_code == 200:
        logger.info(f"Alert sent to Google Chat - {alert_name} - {instance}")
    else:
        logger.error(f"Failed to send message to Google Chat. Status code: {response.status_code}")
        logger.error(f"Response: {response.text}")
