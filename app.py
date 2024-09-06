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
    """
    Function to log system information at regular intervals if logging is enabled in the general settings.
    """
    with app.app_context():  # Push app context for this thread
        try:
            # Fetch general settings once at the beginning
            general_settings = ApplicationGeneralSettings.query.first()
            is_logging_system_info = general_settings.is_logging_system_info if general_settings else False

            logger.info("Is logging system info: %s", is_logging_system_info)
            if not is_logging_system_info:
                logger.warning("Logging is disabled in the settings.")
                return

            while is_logging_system_info:
                logger.debug("Fetching and logging system information.")
                log_data()

                # Sleep for 60 seconds before logging the next set of data
                time.sleep(2)

        except KeyboardInterrupt:
            logger.info("Logging system info interrupted by user.")
        except Exception as e:
            logger.error(f"Error while logging system info: {e}", exc_info=True)


def log_data():
    """
    Function to log system information to the database.
    """
    try:
        system_info = get_system_info_for_db()
        info = SystemInformation(
            cpu_percent=system_info["cpu_percent"],
            memory_percent=system_info["memory_percent"],
            battery_percent=system_info["battery_percent"],
            network_sent=system_info["network_sent"],
            network_received=system_info["network_received"],
            timestamp=datetime.datetime.now(),
        )
        db.session.add(info)
        db.session.commit()
        logger.info("System information logged successfully.")
    except SQLAlchemyError as db_err:
        logger.error(f"Database error: {db_err}")
        db.session.rollback()  # Ensure DB rollback on failure
    except Exception as e:
        logger.error(f"Failed to log system info: {e}", exc_info=True)


if __name__ == "__main__":
    register_routes()

    # Start the system logging thread
    memory_thread = threading.Thread(target=log_system_info, daemon=True)
    memory_thread.start()

    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)
