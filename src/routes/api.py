import psutil
from flask import jsonify, blueprints
from src.config import app
from src.utils import cpu_usage_percent, get_cpu_temp

api_bp = blueprints.Blueprint("api", __name__)


@app.route("/api/system-info/cpu_percent", methods=["GET"])
def cpu_percent():
    cpu_percent = cpu_usage_percent()
    return jsonify({"cpu_percent": cpu_percent})


@app.route("/api/system-info/current_temp", methods=["GET"])
def current_temp():
    current_temp = get_cpu_temp()[0]
    return jsonify({"current_temp": current_temp})

@app.route("/api/system-info/memory_percent", methods=["GET"])
def memory_percent():
    memory_percent = psutil.virtual_memory().percent
    return jsonify({"memory_percent": memory_percent})

@app.route("/api/system-info/disk_percent", methods=["GET"])
def disk_percent():
    disk_percent = psutil.disk_usage('/').percent
    return jsonify({"disk_percent": disk_percent})




#   username = get_cached_value('username', get_system_node_name)
#     ipv4_dict = get_cached_value('ipv4', lambda: get_established_connections()[0])
#     boot_time = get_cached_value('boot_time', lambda: datetime.datetime.fromtimestamp(psutil.boot_time()))
#     uptime_dict = get_cached_value('uptime', lambda: format_uptime(datetime.datetime.now() - boot_time))

#     # Gathering fresh system information
#     battery_info = psutil.sensors_battery()
#     memory_info = psutil.virtual_memory()
#     disk_info = psutil.disk_usage('/')
#     net_io = psutil.net_io_counters(pernic=False)
#     # ifconfig | grep -E 'RX packets|TX packets' -A 1
#     current_server_time = datetime.datetime.now()


# info = {
#         'username': username,
#         'cpu_percent': cpu_usage_percent(),
#         'memory_percent': round(memory_info.percent, 2),
#         'disk_percent': round(disk_info.percent, 2),
#         'battery_percent': round(battery_info.percent, 1) if battery_info else "N/A",
#         'cpu_core': get_cpu_core_count(),
#         'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
#         'network_sent': round(net_io.bytes_sent / CONVERSION_FACTOR_MB, 1),  # In MB
#         'network_received': round(net_io.bytes_recv / CONVERSION_FACTOR_MB, 1),  # In MB
#         'process_count': len(psutil.pids()),
#         'swap_memory': psutil.swap_memory().percent,
#         'ipv4_connections': ipv4_dict,
#         'dashboard_memory_usage': get_flask_memory_usage(),
#         'timestamp': datetime.datetime.now(),
#         'cpu_frequency': get_cpu_frequency(),
#         'current_temp': get_cpu_temp()[0],
#         'current_server_time': datetimeformat(current_server_time),
#     }
#     # update uptime dictionary
#     info.update(uptime_dict)

#     return info
