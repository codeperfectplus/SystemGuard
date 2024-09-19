from flask import Blueprint, Response
from prometheus_client import Counter, Gauge, generate_latest
import threading
import time
from src.config import app
from src.utils import _get_system_info

# Define the Prometheus Blueprint
prometheus_bp = Blueprint('prometheus', __name__)

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
        try:
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
        except Exception as e:
            print(f"Error collecting metrics: {e}")

        # Sleep for 5 seconds before the next collection
        time.sleep(10)

# Start the metrics collection in a background thread
metrics_thread = threading.Thread(target=collect_metrics, daemon=True)
metrics_thread.start()

# Define a route to serve Prometheus metrics
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
