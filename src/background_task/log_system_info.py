import os
import datetime
from threading import Timer
from src.config import app, db
from src.utils import _get_system_info
from src.logger import logger
from src.models import GeneralSettings, SystemInformation
from sqlalchemy.exc import SQLAlchemyError
from src.logger import logger

# Flag to check if logging is already scheduled
is_logging_scheduled = False


def log_system_info():
    """
    Logs system information at regular intervals based on the general settings.
    This function checks if logging is still active before each logging event.
    """
    global is_logging_scheduled
    with app.app_context():
        try:
            # Fetch the general settings to check if logging is enabled
            general_settings = GeneralSettings.query.first()
            is_logging_system_info = (
                general_settings.is_logging_system_info if general_settings else False
            )

            if not is_logging_system_info:
                logger.info("System info logging has been stopped.")
                is_logging_scheduled = False  # Reset the flag if logging stops
                return

            log_system_info_to_db()
            logger.debug("System information logged successfully.")

            # Schedule the next log after 60 seconds
            Timer(60, log_system_info).start()

        except Exception as e:
            logger.error(f"Error during system info logging: {e}", exc_info=True)
            is_logging_scheduled = False  # Reset the flag in case of an error


def log_system_info_to_db():
    """
    Fetches system information and logs it to the database.
    """
    with app.app_context():
        try:
            system_info = _get_system_info()
            system_log = SystemInformation(
                cpu_percent=system_info["cpu_percent"],
                memory_percent=system_info["memory_percent"],
                battery_percent=system_info["battery_percent"],
                network_sent=system_info["network_sent"],
                network_received=system_info["network_received"],
                dashboard_memory_usage=system_info["dashboard_memory_usage"],
                cpu_frequency=system_info["cpu_frequency"],
                current_temp=system_info["current_temp"],
                timestamp=datetime.datetime.now(),
            )
            db.session.add(system_log)
            db.session.commit()
            logger.info("System information logged to database.")

        except SQLAlchemyError as db_err:
            logger.error(
                f"Database error while logging system info: {db_err}", exc_info=True
            )
            db.session.rollback()
        except Exception as e:
            logger.error(f"Failed to log system information: {e}", exc_info=True)

def monitor_settings():
    """
    Monitors application general settings for changes and controls system logging dynamically.
    This function runs periodically to check for updates to logging settings.
    """
    global is_logging_scheduled
    with app.app_context():
        try:
            # Fetch the general settings
            general_settings = GeneralSettings.query.first()

            # Check if logging should be active or not
            is_logging_system_info = (
                general_settings.is_logging_system_info if general_settings else False
            )
            if is_logging_system_info:
                logger.info("System logging enabled. Starting system info logging.")

                # Schedule logging only if not already scheduled
                if not is_logging_scheduled:
                    logger.debug("Scheduling system info logging.")
                    Timer(0, log_system_info).start()
                    is_logging_scheduled = True
            else:
                logger.info("System logging disabled. Stopping system info logging.")
                is_logging_scheduled = False  # Reset the flag if logging is disabled

            # Check settings periodically (every 10 seconds)
            Timer(10, monitor_settings).start()

        except SQLAlchemyError as db_err:
            logger.error(f"Error fetching settings: {db_err}", exc_info=True)

