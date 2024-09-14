from flask import render_template, blueprints, render_template
from flask_login import login_required
from src.config import app
from src.utils import get_established_connections, get_ip_address, get_network_io
from src.routes.helper.common_helper import check_page_toggle

network_info_bp = blueprints.Blueprint("network_stats", __name__)


@app.route("/network_stats")
@login_required
@check_page_toggle("is_network_info_enabled")
def network_stats():
    
    network_sent, network_received = get_network_io()
    _, ipv6_ip = get_established_connections()
    ipv4_ip = get_ip_address()

    system_info = {
        "network_sent": network_sent,
        "network_received": network_received,
        "ipv4_ip": ipv4_ip,
        "ipv6_ip": ipv6_ip,
    }
    
    return render_template("info_pages/network_info.html", system_info=system_info)

