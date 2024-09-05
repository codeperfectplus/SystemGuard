import os
import time
import json
import datetime
import subprocess
import psutil
from flask import render_template_string, jsonify

from src.models import UserDashboardSettings, ApplicationGeneralSettings

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Simple in-memory cache for specific data with individual timestamps
cache = {}
enable_cahce = True
CACHE_EXPIRATION = 3600  # Cache expiration time in seconds (1 hour)


def format_uptime(uptime_seconds):
    """Convert uptime from seconds to a human-readable format."""
    uptime_seconds = uptime_seconds.total_seconds()
    days = int(uptime_seconds // (24 * 3600))
    uptime_seconds %= (24 * 3600)
    hours = int(uptime_seconds // 3600)
    uptime_seconds %= 3600
    minutes = int(uptime_seconds // 60)
    seconds = int(uptime_seconds % 60)
    
    return {
        'uptime_days': days,
        'uptime_hours': hours,
        'uptime_minutes': minutes,
        'uptime_seconds': seconds
    }


def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)

def get_flask_memory_usage():
    """
    Returns the memory usage of the current Flask application in MB.
    """
    try:
        pid = os.getpid()  # Get the current process ID
        process = psutil.Process(pid)  # Get the process information using psutil
        memory_info = process.memory_info()  # Get the memory usage information
        memory_in_mb = memory_info.rss / (1000 ** 2)  # Convert bytes to MB
        return round(memory_in_mb)  # Return the memory usage rounded to 2 decimal places
    except Exception as e:
        print(f"Error getting memory usage: {e}")
        return None

def get_established_connections():
    connections = psutil.net_connections()
    ipv4_set = set()
    ipv6_set = set()

    for conn in connections:
        if conn.status == 'ESTABLISHED':
            if '.' in conn.laddr.ip:
                ipv4_set.add(conn.laddr.ip)
            elif ':' in conn.laddr.ip:
                ipv6_set.add(conn.laddr.ip)

    # ipv4 = [ip for ip in ipv4_set if ip.startswith('192.168')][0] if ipv4_set else "N/A"
    ipv4_set.discard('127.0.0.0')
    print(ipv4_set)
    ipv4 = list(ipv4_set)[0] if ipv4_set else "N/A"
    ipv6 = list(ipv6_set)[0] if ipv6_set else "N/A"

    return ipv4, ipv6

def run_speedtest():
    """ Run a speed test using speedtest-cli. """
    try:
        result = subprocess.run(['speedtest-cli'], capture_output=True, text=True, check=True)
        output_lines = result.stdout.splitlines()
        download_speed, upload_speed, ping = None, None, None

        for line in output_lines:
            if "Download:" in line:
                download_speed = line.split("Download: ")[1]
            elif "Upload:" in line:
                upload_speed = line.split("Upload: ")[1]
            elif "Ping:" in line:
                ping = line.split("Ping: ")[1]

        return {"download_speed": download_speed, "upload_speed": upload_speed, "ping": ping, "status": "Success"}

    except subprocess.CalledProcessError as e:
        return {"status": "Error", "message": e.stderr}

    except Exception as e:
        return {"status": "Error", "message": str(e)}

def get_cpu_frequency():
    return round(psutil.cpu_freq().current)

def get_cpu_core_count():
    return psutil.cpu_count(logical=True)

def cpu_usage_percent():
    return psutil.cpu_percent(interval=1)

def get_cpu_temp():
    try:
        temp = psutil.sensors_temperatures().get('coretemp', [{'current': 'N/A'}])[0]
    except Exception as e:
        temp = {'current_temp': 'N/A', 'high_temp': 'N/A', 'critical_temp': 'N/A'}
    return temp.current, temp.high, temp.critical

def get_top_processes(number=5):
    """Get the top processes by memory usage."""
    processes = [
        (p.info['name'], p.info['cpu_percent'], round(p.info['memory_percent'], 2), p.info['pid'])
        for p in sorted(psutil.process_iter(['name', 'cpu_percent', 'memory_percent', 'pid']),
                        key=lambda p: p.info['memory_percent'], reverse=True)[:number]
    ]
    return processes

def get_disk_free():
    """Returns the free disk space in GB."""
    return round(psutil.disk_usage("/").free / (1000**3), 1)

def get_disk_used():
    """Returns the used disk space in GB."""
    return round(psutil.disk_usage("/").used / (1000**3), 1)

def get_disk_total():
    """Returns the total disk space in GB."""
    return round(psutil.disk_usage("/").total / (1000**3), 1)

def get_disk_usage_percent():
    """Returns the percentage of disk used."""
    disk_usage = psutil.disk_usage("/")
    calculated_percent = (disk_usage.used / disk_usage.total) * 100
    return disk_usage.percent, round(calculated_percent, 1)


def get_memory_available():
    """Returns the available memory in GB."""
    return round(psutil.virtual_memory().total / (1000**3), 2)


def get_memory_used():
    """Returns the used memory in GB."""
    return round((psutil.virtual_memory().total - psutil.virtual_memory().available) / (1000**3), 2)

def get_memory_percent():
    """Returns the percentage of memory used."""
    return psutil.virtual_memory().percent

def get_swap_memory_info():
    """Returns the total, used, and free swap memory in GB."""
    swap = psutil.swap_memory()
    total_swap = swap.total
    used_swap = swap.used
    free_swap = total_swap - used_swap  # Calculate free swap memory

    return {
        "total_swap": round(total_swap / (1000**3), 2),  # In GB
        "used_swap": round(used_swap / (1000**3), 2),    # In GB
        "free_swap": round(free_swap / (1000**3), 2),    # In GB
    }

def render_template_from_file(template_file_path, **context):
    """
    Renders a Jinja template from a file with the given context and returns the rendered HTML content.

    :param template_file_path: Path to the template file to render.
    :param context: Context variables to pass to the template.
    :return: Rendered HTML content as a string.
    """
    # Open and read the template file content
    with open(template_file_path, 'r') as file:
        template_content = file.read()

    # Render the template content with the provided context
    rendered_html = render_template_string(template_content, **context)
    
    return rendered_html


def get_cached_value(key, fresh_value_func):
    """ Get a cached value if available and not expired, otherwise get fresh value. """
    general_settings = ApplicationGeneralSettings.query.first()
    if general_settings:
        enable_cahce = general_settings.enable_cache
    
    current_time = time.time()
    # if key not in cache, create a new entry
    if key not in cache:
        cache[key] = {'value': None, 'timestamp': 0}

    # Check if cache is valid
    if enable_cahce and cache[key]['value'] is not None and (current_time - cache[key]['timestamp'] < CACHE_EXPIRATION):
        # print(key, cache[key]['value'])
        return cache[key]['value']

    # Fetch fresh value
    fresh_value = fresh_value_func()

    # Store value in cache
    cache[key]['value'] = fresh_value
    cache[key]['timestamp'] = current_time

    return fresh_value

def get_system_node_name():
    return os.uname().nodename

def get_system_info():
    """ Get system information with caching for certain values and fresh data for others. """
    username = get_cached_value('username', get_system_node_name)
    ipv4_dict = get_cached_value('ipv4', lambda: get_established_connections()[0])
    boot_time = get_cached_value('boot_time', lambda: datetime.datetime.fromtimestamp(psutil.boot_time()))
    uptime_dict = get_cached_value('uptime', lambda: format_uptime(datetime.datetime.now() - boot_time))

    # Gathering fresh system information
    battery_info = psutil.sensors_battery()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    net_io = psutil.net_io_counters(pernic=False)
    # ifconfig | grep -E 'RX packets|TX packets' -A 1
    current_server_time = datetime.datetime.now()

    # Prepare system information dictionary
    info = {
        'username': username,
        'cpu_percent': cpu_usage_percent(),
        'memory_percent': round(memory_info.percent, 2),
        'disk_usage': round(disk_info.percent, 2),
        'battery_percent': round(battery_info.percent, 1) if battery_info else "N/A",
        'cpu_core': get_cpu_core_count(),
        'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        'network_sent': round(net_io.bytes_sent / (1000 ** 2), 1),  # In MB
        'network_received': round(net_io.bytes_recv / (1000 ** 2), 1),  # In MB
        'process_count': len(psutil.pids()),
        'swap_memory': psutil.swap_memory().percent,
        'ipv4_connections': ipv4_dict,
        'dashboard_memory_usage': get_flask_memory_usage(),
        'timestamp': datetime.datetime.now(),
        'cpu_frequency': get_cpu_frequency(),
        'current_temp': get_cpu_temp()[0],
        'current_server_time': datetimeformat(current_server_time),
    }
    # update uptime dictionary
    info.update(uptime_dict)

    return info

# cpu_percent, memory_percent, battery_percent, network_sent, network_received, timestamp
def get_system_info_for_db():
    """ Get system information for logging in the database. """
    battery_info = psutil.sensors_battery()
    memory_info = psutil.virtual_memory()
    net_io = psutil.net_io_counters(pernic=False)

    # Prepare system information dictionary
    info = {
        'cpu_percent': cpu_usage_percent(),
        'memory_percent': round(memory_info.percent, 2),
        'battery_percent': round(battery_info.percent, 1) if battery_info else "N/A",
        'network_sent': round(net_io.bytes_sent / (1000 ** 2), 1),  # In MB
        'network_received': round(net_io.bytes_recv / (1000 ** 2), 1),  # In MB
        'timestamp': datetime.datetime.now(),
    }

    return info