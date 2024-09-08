import psutil
from flask import jsonify, blueprints
from flask_login import login_required
from src.config import app
from src.models import SystemInformation
from src.utils import cpu_usage_percent, get_cpu_temp, get_cpu_frequency, _get_system_info

api_bp = blueprints.Blueprint("api", __name__)


@app.route("/api/system-info", methods=["GET"])
@login_required
def cpu_percent_api():
    system_info = _get_system_info()
    return jsonify(system_info)


@app.route('/api/graphs_data')
@login_required
def graph_data_api():
    # Query the last 3 entries from the SystemInformation table
    recent_system_info_entries = SystemInformation.query.all()
    
    if recent_system_info_entries:
        # Extract data from the query results
        time_data = [info.timestamp for info in recent_system_info_entries]
        cpu_data = [info.cpu_percent for info in recent_system_info_entries]
        memory_data = [info.memory_percent for info in recent_system_info_entries]
        battery_data = [info.battery_percent for info in recent_system_info_entries]
        network_sent_data = [info.network_sent for info in recent_system_info_entries]
        network_received_data = [info.network_received for info in recent_system_info_entries]
        dashboard_memory_usage = [info.dashboard_memory_usage for info in recent_system_info_entries]
        cpu_frequency = [info.cpu_frequency for info in recent_system_info_entries]
        current_temp = [info.current_temp for info in recent_system_info_entries]
    else:
        time_data = []
        cpu_data = []
        memory_data = []
        battery_data = []
        network_sent_data = []
        network_received_data = []
        dashboard_memory_usage = []
        cpu_frequency = []
        current_temp = []

    return jsonify({
        "time": time_data,
        "cpu": cpu_data,
        "memory": memory_data,
        "battery": battery_data,
        "network_sent": network_sent_data,
        "network_received": network_received_data,
        "dashboard_memory_usage": dashboard_memory_usage,
        "cpu_frequency": cpu_frequency,
        "current_temp": current_temp
    })
