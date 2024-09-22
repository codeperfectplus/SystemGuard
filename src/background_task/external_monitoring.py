from flask import Flask, Response
from prometheus_client import Gauge, generate_latest
import os
import time
from src.models import ExternalMonitornig
from src.config import app
import threading
from src.logger import logger

# Define a Gauge metric with a label 'key' to store multiple values from the file
file_metric = Gauge('external_metrics', 'Value read from file for each key', ['key'])

def read_file_and_update_metric(file_path: str) -> None:    
    """Reads a file and updates metrics based on its content."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    key, value = line.strip().split(':')
                    file_metric.labels(key.strip()).set(float(value.strip()))
                except ValueError as ve:
                    logger.error(f"Value error processing line '{line}': {ve}")
                except Exception as e:
                    logger.error(f"Error processing line '{line}': {e}")
    else:
        logger.warning(f"File {file_path} does not exist")

def fetch_file_metrics(sleep_duration: int = 5) -> None:
    """Background task to read file paths from the database and update metrics."""
    while True:
        with app.app_context():
            file_paths = ExternalMonitornig.query.all()
            current_keys = {sample.labels['key'] for sample in file_metric.collect()[0].samples}
            new_keys = set()

            for file_path in file_paths:
                logger.info(f"Reading file: {file_path.file_path}")
                read_file_and_update_metric(file_path.file_path)
                new_keys.update({key.strip() for line in open(file_path.file_path) for key in line.split(':')[0].strip()})

            # Remove metrics for keys that are no longer in the database
            for key in current_keys:
                if key not in new_keys:
                    file_metric.remove(key)

        time.sleep(sleep_duration)

def fetch_file_metrics_task() -> None:
    """Starts the background task in a separate thread."""
    thread = threading.Thread(target=fetch_file_metrics)
    thread.daemon = True
    thread.start()
