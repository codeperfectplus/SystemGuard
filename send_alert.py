import requests
import json
import time
from src.utils import get_ip_address

def send_test_alert(alertmanager_url, alert_name, severity, instance):
    # Generate a unique alert name by appending the current timestamp
    unique_alert_name = f"{alert_name}_{int(time.time())}"

    # Define the alert data with the unique alert name
    alert_data = [
        {
            "labels": {
                "alertname": unique_alert_name,
                "severity": severity,
                "instance": instance
            },
            "annotations": {
                "description": f"This is a test alert generated at {time.strftime('%Y-%m-%d %H:%M:%S')}",
                "summary": "Test alert to check Slack notifications"
            }
        }
    ]

    # Send the POST request to Alertmanager
    try:
        response = requests.post(
            f"{alertmanager_url}/api/v2/alerts",
            headers={"Content-Type": "application/json"},
            data=json.dumps(alert_data)
        )

        # Log response details
        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        # Check the response
        if response.status_code == 202:
            print(f"Test alert '{unique_alert_name}' sent successfully!")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}, Response: {response.text}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    ip_address = get_ip_address()
    print("IP Address:", ip_address)
    alertmanager_ip = ip_address
    alertmanager_port = "9093"
    alertmanager_url = f"http://{alertmanager_ip}:{alertmanager_port}"

    # Send a test alert with a unique name
    send_test_alert(alertmanager_url, "ScriptAlert", "critical", "instance_name")
