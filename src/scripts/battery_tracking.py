import psutil
import os
from datetime import datetime, timedelta
from src.utils import send_email

STATUS_FILE = 'battery_status.txt'
NOTIFICATION_INTERVAL = timedelta(hours=1)  # Minimum time between notifications

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as file:
            content = file.read().splitlines()
            if len(content) >= 2:
                last_battery_low_time = datetime.fromisoformat(content[0])
                last_notification_time = datetime.fromisoformat(content[1])
                return last_battery_low_time, last_notification_time
    return None, None

def save_status(last_battery_low_time, last_notification_time):
    with open(STATUS_FILE, 'w') as file:
        file.write(f"{last_battery_low_time.isoformat()}\n")
        file.write(f"{last_notification_time.isoformat()}\n")

def check_battery_and_send_message():
    battery = psutil.sensors_battery()
    if battery is None:
        print("Unable to retrieve battery information.")
        return

    battery_percentage = battery.percent
    now = datetime.now()

    last_battery_low_time, last_notification_time = load_status()

    if battery_percentage < 20:
        # Track when the battery was last low
        if last_battery_low_time is None or now - last_battery_low_time > NOTIFICATION_INTERVAL:
            if last_notification_time is None or now - last_notification_time > NOTIFICATION_INTERVAL:
                # Send the email
                receiver_email = "example@example.com"  # Replace with actual email
                subject = "Battery Low Alert"
                body = f"Your battery is critically low at {battery_percentage}%."
                send_email(receiver_email, subject, body)

                # Update the status file
                save_status(now, now)
            else:
                print("Notification interval not yet passed.")
        else:
            print("Battery was recently low; waiting for notification interval.")
    else:
        # Reset status if battery level is above threshold
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)


# import time

# def monitor_battery():
#     while True:
#         check_battery_and_send_message()
#         time.sleep(60 * 10)  # Check every 10 minutes

# if __name__ == "__main__":
#     monitor_battery()
