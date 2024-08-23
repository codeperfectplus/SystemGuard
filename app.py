from flask import Flask, render_template
import os
import psutil
import datetime

app = Flask(__name__)

def get_established_connections():
    connection = psutil.net_connections()
    ipv4_dict = {}
    ipv6_dict = {}

    for conn in connection:
        if conn.status == 'ESTABLISHED':
            if '.' in conn.laddr.ip:
                ipv4_dict = conn.laddr.ip
            elif ':' in conn.laddr.ip:
                ipv6_dict = conn.laddr.ip

    return ipv4_dict, ipv6_dict

def change_up_time_format(uptime):
    uptime_seconds = uptime.total_seconds()
    days = int(uptime_seconds // (24 * 3600))
    uptime_seconds %= (24 * 3600)
    hours = int(uptime_seconds // 3600)
    uptime_seconds %= 3600
    minutes = int(uptime_seconds // 60)
    return f"{days} days, {hours} hours, {minutes} minutes"

def get_system_info():
    info = {
        'username': os.getlogin(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'battery_percent': round(psutil.sensors_battery().percent) if psutil.sensors_battery() else "N/A",
        'cpu_core': psutil.cpu_count(),
        'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        'network_sent': round(psutil.net_io_counters().bytes_sent / (1024 ** 2), 2),  # In MB
        'network_received': round(psutil.net_io_counters().bytes_recv / (1024 ** 2), 2),  # In MB
        'process_count': len(psutil.pids()),
        'swap_memory': psutil.swap_memory().percent,
        'uptime': change_up_time_format(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time()))
    }

    ipv4_conn, ipv6_conn = get_established_connections()
    info['ipv4_connections'] = ipv4_conn
    info['ipv6_connections'] = ipv6_conn
    return info

@app.route('/')
def dashboard():
    system_info = get_system_info()
    return render_template('dashboard.html', system_info=system_info)

@app.route('/cpu_usage')
def cpu_usage():
    # Detailed CPU usage stats
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    return render_template('cpu_usage.html', cpu_usage=cpu_usage)

@app.route('/memory_usage')
def memory_usage():
    memory_info = {
        'memory_percent': psutil.virtual_memory().percent,
        'memory_available': round(psutil.virtual_memory().available / (1024 ** 3), 2),  # In GB
        'memory_used': round(psutil.virtual_memory().used / (1024 ** 3), 2)  # In GB
    }
    return render_template('memory_usage.html', memory_info=memory_info)

@app.route('/disk_usage')
def disk_usage():
    disk_info = {
        'disk_usage': psutil.disk_usage('/').percent,
        'disk_total': round(psutil.disk_usage('/').total / (1024 ** 3), 2),  # In GB
        'disk_used': round(psutil.disk_usage('/').used / (1024 ** 3), 2),  # In GB
        'disk_free': round(psutil.disk_usage('/').free / (1024 ** 3), 2)  # In GB
    }
    return render_template('disk_usage.html', disk_info=disk_info)

@app.route('/network_stats')
def network_stats():
    net_io = psutil.net_io_counters()
    network_info = {
        'network_sent': round(net_io.bytes_sent / (1024 ** 2), 2),  # In MB
        'network_received': round(net_io.bytes_recv / (1024 ** 2), 2)  # In MB
    }
    return render_template('network_stats.html', network_info=network_info)

@app.route('/system_health')
def system_health():
    # Reuse system_info function for summary
    system_info = get_system_info()
    return render_template('system_health.html', system_info=system_info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
