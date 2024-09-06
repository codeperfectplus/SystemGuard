import os
import time
import datetime
import threading
from src.config import app, db
from src import routes
from src.utils import get_system_info_for_db
from src.models import SystemInformation, ApplicationGeneralSettings
from src.scripts.email_me import send_smpt_email
from flask import current_app

def register_routes():
    app.register_blueprint(routes.dashboard_bp)
    app.register_blueprint(routes.settings_bp)
    app.register_blueprint(routes.system_health_bp)
    app.register_blueprint(routes.cpu_info_bp)
    app.register_blueprint(routes.disk_info_bp)
    app.register_blueprint(routes.memory_info_bp)
    app.register_blueprint(routes.network_info_bp)
    app.register_blueprint(routes.speedtest_bp)
    app.register_blueprint(routes.process_bp)

def log_system_info():
    with app.app_context():  # Ensure Flask app context is available
        general_settings = ApplicationGeneralSettings.query.first()
        is_logging_system_info = general_settings.is_logging_system_info
        print("Is logging system info: ", is_logging_system_info)
        if not is_logging_system_info:
            return 
        while True:
                system_info = get_system_info_for_db()
                info = SystemInformation(
                    cpu_percent=system_info["cpu_percent"],
                    memory_percent=system_info["memory_percent"],
                    battery_percent=system_info["battery_percent"],
                    network_sent=system_info["network_sent"],
                    network_received=system_info["network_received"],
                    timestamp=datetime.datetime.now(),
                )
                print("Logging system information")
                db.session.add(info)
                db.session.commit()  # Commit to save the data in the database
                time.sleep(60)

if __name__ == "__main__":
    register_routes()

    # Start the memory-consuming program in a separate thread
    memory_thread = threading.Thread(target=log_system_info, daemon=True)
    memory_thread.start()

    # Run the Flask application
    app.run(host="0.0.0.0", port=5000)
