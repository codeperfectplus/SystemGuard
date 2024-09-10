import os
import datetime
from threading import Timer
from flask import url_for
from src.config import app, db
from src.utils import _get_system_info
from src.logger import logger
from src.models import MonitoredWebsite, GeneralSettings, SystemInformation
from sqlalchemy.exc import SQLAlchemyError
import requests
from src.scripts.email_me import send_smtp_email
from src.logger import logger
from src.utils import render_template_from_file, ROOT_DIR
from src.config import get_app_info

# Dictionary to track the last known status of each website
website_status = {}
# Flag to check if logging is already scheduled
is_logging_scheduled = False


def send_mail(website_name, status, email_adress, email_alerts_enabled):
    """
    Dummy function to simulate sending an email.

    Args:
        website_name (str): The name or URL of the website.
        status (str): The status of the website, either 'DOWN' or 'UP'.
    """
    # This is a dummy function, so no real email is sent.
    if email_alerts_enabled:
        context = {
            "website_status": status,  # UP/DOWN
            "website_name": website_name,
            "checked_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": f"{website_name} is now {status}",
            "title": get_app_info()["title"],
        }
        website_status_template = os.path.join(
            ROOT_DIR, "src/templates/email_templates/website_monitor_status.html"
        )
        email_subject = f"{website_name} is now {status}"
        email_body = render_template_from_file(website_status_template, **context)
        send_smtp_email(email_adress, email_subject, email_body, is_html=True)


def update_website_status(website, status):
    """
    Updates the status of the website and sends an email notification if the status has changed.

    Args:
        website (MonitoredWebsite): The website object to update.
        status (str): The new status of the website.
    """
    global website_status

    if website.id not in website_status:
        website_status[website.id] = "UP"  # Initialize with UP status if not present

    if website_status[website.id] != status:
        send_mail(
            website.name, status, website.email_address, website.email_alerts_enabled
        )
        website_status[website.id] = status


def ping_website(website):
    """
    Pings a single website and updates its status in the database.

    Args:
        website (MonitoredWebsite): The website object to ping.
    """
    with app.app_context():
        try:
            # Check if the website is still active
            updated_website = MonitoredWebsite.query.get(website.id)
            if not updated_website or not updated_website.is_ping_active:
                logger.info(
                    f"Website {website.name} is no longer active. Stopping monitoring."
                )
                return

            logger.info(
                f"Pinging {website.name} (Interval: {website.ping_interval}s)..."
            )
            response = requests.get(website.name, timeout=10)
            updated_website.last_ping_time = datetime.datetime.now()
            updated_website.ping_status_code = response.status_code

            new_status = "UP" if response.status_code == 200 else "DOWN"
            updated_website.ping_status = new_status

            # Update the website status
            db.session.commit()
            logger.info(f"Website {website.name} updated successfully.")

            # Determine if an email should be sent
            update_website_status(website, new_status)

        except requests.RequestException as req_err:
            updated_website.ping_status = "DOWN"
            logger.error(f"Failed to ping {website.name}: {req_err}", exc_info=True)
            db.session.rollback()

        except SQLAlchemyError as db_err:
            logger.error(
                f"Database commit error for {website.name}: {db_err}", exc_info=True
            )
            db.session.rollback()

        finally:
            # Add more detailed logging for debugging
            if db.session.new or db.session.dirty:
                logger.warning(
                    f"Database transaction not committed properly for {website.name}."
                )

            # Schedule the next ping for this website
            Timer(
                updated_website.ping_interval, ping_website, args=[updated_website]
            ).start()


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


def start_website_monitoring():
    """
    Periodically pings monitored websites based on individual ping intervals.
    """
    with app.app_context():
        try:
            while True:
                active_websites = MonitoredWebsite.query.filter_by(
                    is_ping_active=True
                ).all()
                if not active_websites:
                    logger.info("No active websites to monitor.")
                else:
                    for website in active_websites:
                        # Start pinging each website individually based on its ping interval
                        Timer(0, ping_website, args=[website]).start()

                # Check for active websites periodically (every 30 seconds)
                Timer(30, start_website_monitoring).start()
                break  # Break out of the loop to avoid creating a new thread infinitely

        except SQLAlchemyError as db_err:
            logger.error(
                f"Database error during website monitoring: {db_err}", exc_info=True
            )
        except Exception as e:
            logger.error(f"Error during website monitoring: {e}", exc_info=True)
