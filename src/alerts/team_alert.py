import requests
import json

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
        print("Alert sent successfully to Microsoft Teams!")
    else:
        print(f"Failed to send alert. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Example usage:
# if __name__ == "__main__":
#     # Replace with your Microsoft Teams webhook URL
#     webhook_url = "https://outlook.office.com/webhook/YOUR_WEBHOOK_URL"
    
#     # Define the alert details
#     alert_name = "CPU Usage High"
#     instance = "server-01"
#     severity = "critical"
#     description = "CPU usage is over 90% for more than 5 minutes."

#     # Send the alert
#     send_teams_alert(webhook_url, alert_name, instance, severity, description)
