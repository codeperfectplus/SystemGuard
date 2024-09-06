import logging
from logging.handlers import RotatingFileHandler
import os

# Create a logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Log Formatter with datetime, log level, and message
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File handler for logging to a file
file_handler = RotatingFileHandler(
    'logs/app_debug.log', 
    maxBytes=10 * 1024 * 1024,  # 10 MB per log file
    backupCount=5  # Keep up to 5 old log files
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Log everything (DEBUG, INFO, WARNING, etc.)
logger.addHandler(file_handler)

# Optionally, add console output for real-time debugging (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
