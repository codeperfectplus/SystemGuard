import os
import time
import datetime
import threading
from src.config import app, db
from src import routes
from src.utils import get_system_info_for_db
from src.models import SystemInformation
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

app.config['is_server_up_email_sent'] = False

def log_system_info():
    while True:
        with app.app_context():  # Ensure Flask app context is available
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
    app.run(host="0.0.0.0", port=5000, debug=True)
