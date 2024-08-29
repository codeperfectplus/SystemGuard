import psutil
from flask import render_template, blueprints

from src.config import app
from src.utils import get_established_connections
network_stats_bp = blueprints.Blueprint("network_stats", __name__)

@app.route("/network_stats")
def network_stats():
    net_io = psutil.net_io_counters()
    ipv4_ip, ipv6_ip = get_established_connections()
    network_info = {
        "network_sent": round(net_io.bytes_sent / (1024**2), 2),  # In MB
        "network_received": round(net_io.bytes_recv / (1024**2), 2),  # In MB
        "ipv4_ip": ipv4_ip,
        "ipv6_ip": ipv6_ip,
    }
    return render_template("network_stats.html", network_info=network_info)

