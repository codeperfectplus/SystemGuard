import os
from src.background_task.monitor_website import start_website_monitoring
from src.background_task.log_system_info import monitor_settings
from src.background_task.external_monitoring import fetch_file_metrics_task
from src.logger import logger



def start_background_tasks():
    """
    Starts the background tasks for the application.
    """
    if os.getenv('FLASK_ENV') == 'production':
        logger.info("Starting background tasks for production environment.")
        start_website_monitoring()
        fetch_file_metrics_task()
        monitor_settings()
    else:
        logger.info("Background tasks are not started in development environment.")