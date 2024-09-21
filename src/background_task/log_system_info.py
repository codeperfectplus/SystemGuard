import os
import datetime
from threading import Timer
from src.config import app, db
from src.utils import _get_system_info
from src.logger import logger
from src.models import GeneralSettings, SystemInformation
from sqlalchemy.exc import SQLAlchemyError
from prometheus_client import Counter, Gauge
import os

from src.logger import logger
# Flag to track if logging is already scheduled
is_logging_scheduled = False
fetch_system_info_interval = 30

# Initialize Prometheus metrics
metrics = {
    'cpu_usage_metric': Gauge('cpu_usage_percentage', 'Current CPU usage percentage'),
    'memory_usage_metric': Gauge('memory_usage_percentage', 'Current memory usage percentage'),
    'disk_usage_metric': Gauge('disk_usage_percentage', 'Disk usage percentage'),
    'network_sent_metric': Gauge('network_bytes_sent', 'Total network bytes sent'),
    'network_recv_metric': Gauge('network_bytes_received', 'Total network bytes received'),
    'cpu_temp_metric': Gauge('cpu_temperature', 'Current CPU temperature'),
    'cpu_frequency_metric': Gauge('cpu_frequency', 'Current CPU frequency'),
    'battery_percentage_metric': Gauge('battery_percentage', 'Current battery percentage'),
    'dashboard_memory_usage_metric': Gauge('dashboard_memory_usage_percentage', 'Current memory usage percentage'),
    'request_count': Counter('http_requests_total', 'Total HTTP requests made')
}

def log_system_info():
    """
    Logs system information at regular intervals based on the general settings.
    This function checks if logging is enabled and schedules the next log if active.
    """
    global is_logging_scheduled
    with app.app_context():
        try:
            if not is_logging_enabled():
                logger.info("System info logging has been stopped.")
                is_logging_scheduled = False
                return

            log_system_info_to_db()
            logger.debug("System information logged successfully.")
            schedule_next_log(interval=fetch_system_info_interval)

        except Exception as e:
            logger.error(f"Error during system info logging: {e}", exc_info=True)
            is_logging_scheduled = False


def is_logging_enabled():
    """
    Checks if system info logging is enabled in the general settings.
    """
    try:
        general_settings = GeneralSettings.query.first()
        return general_settings.is_logging_system_info if general_settings else False
    except SQLAlchemyError as e:
        logger.error(f"Error fetching general settings: {e}", exc_info=True)
        return False


def schedule_next_log(interval=10):
    """
    Schedules the next logging event after the specified interval (in seconds).
    """
    Timer(interval, log_system_info).start()


def log_system_info_to_db():
    """
    Fetches system information and logs it to the database and updates Prometheus metrics.
    """
    with app.app_context():
        try:
            system_info = _get_system_info()

            # Update Prometheus metrics
            update_prometheus_metrics(system_info)

            # Store system information in InfluxDB
            # store_system_info_in_influxdb(system_info)

            # Store system information in the database
            # store_system_info_in_db(system_info)
            logger.info("System information logged to database.")

        except SQLAlchemyError as db_err:
            logger.error(f"Database error while logging system info: {db_err}", exc_info=True)
            db.session.rollback()
        except Exception as e:
            logger.error(f"Failed to log system information: {e}", exc_info=True)


def update_prometheus_metrics(system_info):
    """
    Updates Prometheus metrics with the latest system information.
    """
    metrics['cpu_usage_metric'].set(system_info['cpu_percent'])
    metrics['memory_usage_metric'].set(system_info['memory_percent'])
    metrics['disk_usage_metric'].set(system_info['disk_percent'])
    metrics['network_sent_metric'].set(system_info['network_sent'])
    metrics['network_recv_metric'].set(system_info['network_received'])
    metrics['cpu_temp_metric'].set(system_info['current_temp'])
    metrics['cpu_frequency_metric'].set(system_info['cpu_frequency'])
    metrics['battery_percentage_metric'].set(system_info['battery_percent'])
    metrics['dashboard_memory_usage_metric'].set(system_info['dashboard_memory_usage'])
    metrics['request_count'].inc()


def store_system_info_in_db(system_info):
    """
    Stores the collected system information into the database.
    """
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

# def store_system_info_in_influxdb(system_info):
#     """
#     Stores the collected system information into the InfluxDB with proper error handling.
#     """
#     try:
#         # Create a data point for system information
#         point = (
#             Point("system_info")
#             .tag("host", get_system_username())
#             .field("cpu_percent", system_info["cpu_percent"])
#             .field("memory_percent", system_info["memory_percent"])
#             .field("battery_percent", system_info["battery_percent"])
#             .field("network_sent", system_info["network_sent"])
#             .field("network_received", system_info["network_received"])
#             .field("dashboard_memory_usage", system_info["dashboard_memory_usage"])
#             .field("cpu_frequency", system_info["cpu_frequency"])
#             .field("current_temp", system_info["current_temp"])
#             .time(int(time.time() * 1_000_000_000))
#         )

#         # Write the data point to InfluxDB
#         write_api.write(bucket=bucket, record=point)
#         logger.info("Successfully wrote system information to InfluxDB")

#     except ValueError as ve:
#         logger.error(f"Value error while storing system info: {ve}")
#     except Exception as e:
#         logger.error(f"An unexpected error occurred: {e}", exc_info=True)



def monitor_settings():
    """
    Monitors application general settings for changes and controls system logging dynamically.
    """
    global is_logging_scheduled
    with app.app_context():
        try:
            if is_logging_enabled():
                logger.info("System logging enabled. Starting system info logging.")
                if not is_logging_scheduled:
                    logger.debug("Scheduling system info logging.")
                    Timer(0, log_system_info).start()
                    is_logging_scheduled = True
            else:
                logger.info("System logging disabled. Stopping system info logging.")
                is_logging_scheduled = False

            # Recheck settings every 10 seconds
            Timer(30, monitor_settings).start()

        except SQLAlchemyError as db_err:
            logger.error(f"Error fetching settings: {db_err}", exc_info=True)
