import requests
import json

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
                    "title": summary,
                    "subtitle": f"Alert: {alert_name}",
                    "imageUrl": "https://example.com/icon.png"  # Optionally, replace with a relevant icon
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "keyValue": {
                                    "topLabel": "Instance",
                                    "content": instance
                                }
                            },
                            {
                                "keyValue": {
                                    "topLabel": "Severity",
                                    "content": severity,
                                    "icon": "ALERT"
                                }
                            },
                            {
                                "keyValue": {
                                    "topLabel": "Description",
                                    "content": description
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
        print("Message sent successfully to Google Chat!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Example usage:
# webhook_url = "https://chat.googleapis.com/v1/spaces/XXXXXX/messages?key=XXXXX&token=XXXXX"
# send_google_chat_alert(webhook_url, "CPU High Usage", "server-01", "critical", "The CPU usage is above 90% for 5 minutes.", "Prometheus Alert")
