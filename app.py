from flask import Flask, render_template
import os
import psutil, datetime

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
        'uptime': datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    }

    ipv4_conn, ipv6_conn = get_established_connections()
    info['ipv4_connections'] = ipv4_conn
    info['ipv6_connections'] = ipv6_conn
    return info


@app.route('/')
def dashboard():
    system_info = get_system_info()
    return render_template('dashboard.html', system_info=system_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
