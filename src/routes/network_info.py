import psutil
from flask import render_template, blueprints, flash
from flask_login import login_required
from src.config import app
from src.utils import get_established_connections
from src.models import  PageToggleSettings

network_info_bp = blueprints.Blueprint("network_stats", __name__)

@app.route("/network_stats")
@login_required
def network_stats():
    page_toggles_settings = PageToggleSettings.query.first()
    if not page_toggles_settings.is_network_info_enabled:
        flash("You do not have permission to view this page.", "danger")
        return render_template("error/403.html")
    net_io = psutil.net_io_counters()
    ipv4_ip, ipv6_ip = get_established_connections()
    system_info = {
        "network_sent": round(net_io.bytes_sent / (1024**2), 2),  # In MB
        "network_received": round(net_io.bytes_recv / (1024**2), 2),  # In MB
        "ipv4_ip": ipv4_ip,
        "ipv6_ip": ipv6_ip,
    }
    return render_template("info_pages/network_info.html", system_info=system_info)

