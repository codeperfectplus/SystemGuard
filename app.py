from src.config import app
from src import routes
from src.background_task import start_website_monitoring, monitor_settings, fetch_file_metrics_task
import os

# background thread to monitor system settings changes
# print("FLASK_ENV: ", os.getenv('FLASK_ENV'))
# # if os.getenv('FLASK_ENV') == 'production':
# start_website_monitoring()  # Starts pinging active websites
# fetch_file_metrics_task()
monitor_settings()  # Starts monitoring for system logging changes

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
