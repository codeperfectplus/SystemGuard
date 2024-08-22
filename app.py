from flask import Flask, render_template
import os
import psutil

app = Flask(__name__)

def get_system_info():
    info = {
        'username': os.getlogin(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'battery_percent': psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A",
    }
    return info

@app.route('/')
def dashboard():
    system_info = get_system_info()
    return render_template('dashboard.html', system_info=system_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
