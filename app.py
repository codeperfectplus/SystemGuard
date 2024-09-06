import os
import time
import datetime
import threading
from src.config import app, db
from src import routes
from src.utils import get_system_info_for_db
from src.models import SystemInformation, ApplicationGeneralSettings
from sqlalchemy.exc import SQLAlchemyError
from src.logger import logger
from src.thread_process import monitor_settings, start_website_monitoring

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





if __name__ == "__main__":
    register_routes()

        # Start monitoring settings and website pinging when the server starts
    monitor_settings()  # Starts monitoring for system logging changes
    start_website_monitoring()  # Starts pinging active websites

    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)
