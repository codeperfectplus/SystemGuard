import requests
from src.logger import logger

def send_alert_to_discord(webhook_url, alert_name, instance, severity, description, summary):
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
    message = {
        "content": f"**{alert_name}**\n"
                   f"**Instance:** {instance}\n"
                   f"**Severity:** {severity}\n"
                   f"**Summary:** {summary}\n"
                   f"**Description:** {description}"
    }

    # Sending the message to Discord
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()  # Raise an error for bad responses
        logger.info(f"Alert sent to Discord: {alert_name} - {instance}")
        return True
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while sending alert: {http_err}")
    except Exception as err:
        logger.error(f"An error occurred while sending alert: {err}")

    return False

# # Example usage
# if __name__ == "__main__":
#     webhook_url = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
    
#     # Sample alert data
#     alert_name = "High CPU Usage"
#     instance = "server1"
#     severity = "critical"
#     description = "CPU usage has exceeded 90%"
#     summary = "High CPU usage detected"
    
#     success = send_alert_to_discord(webhook_url, alert_name, instance, severity, description, summary)
#     if success:
#         logger.info("Alert sent successfully.")
#     else:
#         logger.error("Failed to send alert.")
