from flask import blueprints
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Counter, Gauge
import threading
import time
from src.config import app
from src.utils import _get_system_info

# Define the Prometheus Blueprint
prometheus_bp = blueprints.Blueprint('prometheus', __name__)

# Initialize Prometheus metrics
cpu_usage_metric = Gauge('cpu_usage_percentage', 'Current CPU usage percentage')
memory_usage_metric = Gauge('memory_usage_percentage', 'Current memory usage percentage')
disk_usage_metric = Gauge('disk_usage_percentage', 'Disk usage percentage')
network_sent_metric = Gauge('network_bytes_sent', 'Total network bytes sent')
network_recv_metric = Gauge('network_bytes_received', 'Total network bytes received')
request_count = Counter('http_requests_total', 'Total HTTP requests made')

def collect_metrics():
    """
    Collect system metrics and update Prometheus Gauges.
    Runs in a separate thread and updates metrics every 5 seconds.
    """
    while True:
        # Gather system information
        system_info = _get_system_info()

        # Update Prometheus metrics
        cpu_usage_metric.set(system_info['cpu_percent'])
        memory_usage_metric.set(system_info['memory_percent'])
        disk_usage_metric.set(system_info['disk_percent'])
        network_sent_metric.set(system_info['network_sent'])
        network_recv_metric.set(system_info['network_received'])

        # Increment HTTP request counter
        request_count.inc()

        # Sleep for 5 seconds before the next collection
        time.sleep(5)

# Start the metrics collection in a background thread
metrics_thread = threading.Thread(target=collect_metrics, daemon=True)
metrics_thread.start()

# Expose the /metrics endpoint for Prometheus to scrape metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()  # Serve Prometheus metrics at /metrics
})
