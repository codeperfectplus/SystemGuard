import requests
import json

def send_teams_message(webhook_url, message_title="SystemGuard Alert", message_body=""):
    """
    Sends a message to a Microsoft Teams channel using a webhook.

    Parameters:
    webhook_url (str): The webhook URL of the Teams channel.
    message_title (str): The title of the message (appears bold).
    message_body (str): The content/body of the message.
    """

    # Define the message payload
    message_payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": message_title,
        "themeColor": "0076D7",  # Can change the theme color of the card
        "sections": [{
            "activityTitle": message_title,
            "text": message_body
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
        print("Message sent successfully to Microsoft Teams!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Example usage:
if __name__ == "__main__":
    # Replace with your Microsoft Teams webhook URL
    webhook_url = "https://outlook.office.com/webhook/YOUR_WEBHOOK_URL"
    
    # Define the message content
    message_title = "SystemGuard Alert"
    message_body = "This is a notification about an important system event."

    # Send the message
    send_teams_message(webhook_url, message_title, message_body)
