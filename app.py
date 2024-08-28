from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import psutil
import datetime
import subprocess

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speedtest_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the model for storing speed test results
class SpeedTestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    download_speed = db.Column(db.String(50))
    upload_speed = db.Column(db.String(50))
    ping = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

    def __repr__(self):
        return f'<SpeedTestResult {self.download_speed}, {self.upload_speed}, {self.ping}>'

def change_up_time_format(uptime):
    uptime_seconds = uptime.total_seconds()
    days = int(uptime_seconds // (24 * 3600))
    uptime_seconds %= (24 * 3600)
    hours = int(uptime_seconds // 3600)
    uptime_seconds %= 3600
    minutes = int(uptime_seconds // 60)
    return f"{days} days, {hours} hours, {minutes} minutes"

def run_speedtest():
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
        
        return {"download_speed": download_speed, "upload_speed": upload_speed, "ping": ping}
    
    except subprocess.CalledProcessError as e:
        print(f"Speedtest failed with error: {e.stderr}")
        return None
    
    except Exception as e:
        print(f"Error occurred while running speed test: {e}")
        return None

@app.route('/speedtest')
def speedtest():
    one_hour_ago = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    recent_results = SpeedTestResult.query.filter(SpeedTestResult.timestamp > one_hour_ago).all()

    if len(recent_results) < 3:
        speedtest_result = run_speedtest()
        if speedtest_result:
            new_result = SpeedTestResult(
                download_speed=speedtest_result['download_speed'],
                upload_speed=speedtest_result['upload_speed'],
                ping=speedtest_result['ping']
            )
            db.session.add(new_result)
            db.session.commit()
            return render_template('speedtest_result.html', speedtest_result=speedtest_result, source="Actual Test")
    else:
        latest_result = recent_results[-1]
        next_test_time = latest_result.timestamp + datetime.timedelta(hours=1)
        return render_template('speedtest_result.html', 
                               speedtest_result=latest_result, 
                               source="Database", 
                               next_test_time=next_test_time)

def get_system_info():
    print("Getting system information...")
    ipv4_dict, ipv6_dict = get_established_connections()
    info = {
        'username': os.getlogin(),
        'cpu_percent': round(psutil.cpu_percent(interval=1), 2),
        'memory_percent': round(psutil.virtual_memory().percent, 2),
        'disk_usage': round(psutil.disk_usage('/').percent, 2),
        'battery_percent': round(psutil.sensors_battery().percent) if psutil.sensors_battery() else "N/A",
        'cpu_core': psutil.cpu_count(),
        'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        'network_sent': round(psutil.net_io_counters().bytes_sent / (1024 ** 2), 2),  # In MB
        'network_received': round(psutil.net_io_counters().bytes_recv / (1024 ** 2), 2),  # In MB
        'process_count': len(psutil.pids()),
        'swap_memory': psutil.swap_memory().percent,
        'uptime': change_up_time_format(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())),
        'ipv4_connections': ipv4_dict,
        'ipv6_connections': ipv6_dict
    }
    return info

def get_established_connections():
    connections = psutil.net_connections()
    ipv4_dict = set()
    ipv6_dict = set()

    for conn in connections:
        if conn.status == 'ESTABLISHED':
            if '.' in conn.laddr.ip:
                ipv4_dict.add(conn.laddr.ip)
            elif ':' in conn.laddr.ip:
                ipv6_dict.add(conn.laddr.ip)

    ipv4_dict = [ip for ip in ipv4_dict if ip.startswith('192.168')]
    return ipv4_dict[0] if ipv4_dict else "N/A", ipv6_dict

@app.route('/')
def dashboard():
    system_info = get_system_info()
    return render_template('dashboard.html', system_info=system_info)

@app.route('/cpu_usage')
def cpu_usage():
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
    system_info = get_system_info()
    return render_template('system_health.html', system_info=system_info)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
