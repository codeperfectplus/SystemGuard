import os
import datetime
import subprocess
import psutil

from src.config import app, db
from src.models import SystemInfo

def format_uptime(uptime_seconds):
    """Convert uptime from seconds to a human-readable format."""
    uptime_seconds = uptime_seconds.total_seconds()
    days = int(uptime_seconds // (24 * 3600))
    uptime_seconds %= (24 * 3600)
    hours = int(uptime_seconds // 3600)
    uptime_seconds %= 3600
    minutes = int(uptime_seconds // 60)
    return f"{days} days, {hours} hours, {minutes} minutes"


def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)

def get_flask_memory_usage():
    """
    Returns the memory usage of the current Flask application in MB.
    """
    pid = os.getpid()
    process = psutil.Process(pid)
    memory_info = process.memory_info()
    memory_in_mb = memory_info.rss / (1024 ** 2)
    return f"{round(memory_in_mb)} MB"

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

    # ipv4_dict = [ip for ip in ipv4_dict if ip.startswith('192.168')]
    # return ipv4_dict[0] if ipv4_dict else "N/A", ipv6_dict
    ipv4 = [ip for ip in ipv4_set if ip.startswith('192.168')][0]
    ipv6 = list(ipv6_set)[0]

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

        return {"download_speed": download_speed, "upload_speed": upload_speed, "ping": ping,
                "status": "Success"}

    except subprocess.CalledProcessError as e:
        error = {"status": "Error", "message": e.stderr}
        return error

    except Exception as e:
        error = {"status": "Error", "message": str(e)}
        return error

def get_cpu_frequency():
    cpu_freq = psutil.cpu_freq().current  # In MHz
    return round(cpu_freq)

def swap_memory_info():
    swap = psutil.swap_memory()
    swap_total = swap.total
    swap_used = swap.used
    swap_percent = swap.percent
    return swap_total, swap_used, swap_percent

def get_cpu_core_count():
    return psutil.cpu_count(logical=True)

def cpu_usage_percent():
    return round(psutil.cpu_percent(interval=1), 2)

def get_cpu_temp():
    temp = psutil.sensors_temperatures().get('coretemp', [{'current': 'N/A'}])[0]
    current_temp = temp.current
    high_temp = temp.high
    critical_temp = temp.critical
    return current_temp, high_temp, critical_temp

def get_system_info():
    """ Get system information and store it in the database. """
    print("Getting system information...")

    # Gathering system information
    ipv4_dict, _ = get_established_connections()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = format_uptime(datetime.datetime.now() - boot_time)
    battery_info = psutil.sensors_battery()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()

    # Prepare system information dictionary
    info = {
        'username': os.getlogin(),
        'cpu_percent': cpu_usage_percent(),
        'memory_percent': round(memory_info.percent, 2),
        'disk_usage': round(disk_info.percent, 2),
        'battery_percent': round(battery_info.percent) if battery_info else "N/A",
        'cpu_core': get_cpu_core_count(),
        'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        'network_sent': round(net_io.bytes_sent / (1024 ** 2), 2),  # In MB
        'network_received': round(net_io.bytes_recv / (1024 ** 2), 2),  # In MB
        'process_count': len(psutil.pids()),
        'swap_memory': psutil.swap_memory().percent,
        'uptime': uptime,
        'ipv4_connections': ipv4_dict,
        'dashboard_memory_usage': get_flask_memory_usage(),
        'timestamp': datetime.datetime.now(),
        'cpu_frequency': get_cpu_frequency(),
        'current_temp': get_cpu_temp()[0],
    }

    # # Adding system info to the database
    # with app.app_context():
    #     db.session.add(SystemInfo(**info))
    #     db.session.commit()

    return info
