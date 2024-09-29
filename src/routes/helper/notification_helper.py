import requests
import json
import time


def send_test_alert(alertmanager_url, alert_name, severity, instance):
    # Generate a unique alert name by appending the current timestamp
    unique_alert_name = f"{alert_name}_{int(time.time())}"

    # Define the alert data with the unique alert name
    alert_data = [
        {
            "labels": {
                "alertname": unique_alert_name,
                "severity": severity,
                "instance": instance,
            },
            "annotations": {
                "description": f"This is a test alert generated at {time.strftime('%Y-%m-%d %H:%M:%S')}",
                "summary": "Test alert to check Slack notifications",
            },
        }
    ]

    # Send the POST request to Alertmanager
    try:
        response = requests.post(
            f"{alertmanager_url}/api/v2/alerts",
            headers={"Content-Type": "application/json"},
            data=json.dumps(alert_data),
        )

        # Log response details
        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        # Check the response
        if response.status_code == 202 or response.status_code == 200:
            return {
                "message": f"Test alert '{unique_alert_name}' sent successfully!",
                "status": 200,
            }
        else:
            return {
                "message": f"Failed to send alert, Response: {response.text}",
                "status": response.status_code,
            }

    except Exception as e:
        return {"message": f"An error occurred: {e}", "status": 500}
