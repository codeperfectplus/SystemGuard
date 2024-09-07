from src.config import app
from src import routes
from src.thread_process import monitor_settings, start_website_monitoring

if __name__ == "__main__":

    # background thread to monitor system settings changes
    # monitor_settings()  # Starts monitoring for system logging changes
    # start_website_monitoring()  # Starts pinging active websites

    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)
