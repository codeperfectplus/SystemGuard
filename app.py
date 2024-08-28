from flask import render_template, request, flash
import os
import psutil
import datetime
import subprocess
from src.config import app, db
from src.models import SpeedTestResult, DashoardSettings, SystemInfo
from src.utils import (
    datetimeformat, 
    run_speedtest,
    get_system_info
)

# initialize the database
with app.app_context():
    db.create_all()
    settings = DashoardSettings.query.first()
    if not settings:
        db.session.add(DashoardSettings())
        db.session.commit()

@app.route('/')
def dashboard():
    settings = DashoardSettings.query.first()
    SPEEDTEST_COOLDOWN_IN_HOURS = settings.speedtest_cooldown
    system_info = get_system_info(SystemInfo=SystemInfo)
    
    # Fetch the last speedtest result
    n_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=SPEEDTEST_COOLDOWN_IN_HOURS)
    recent_results = SpeedTestResult.query.filter(SpeedTestResult.timestamp > n_hour_ago).all()
    last_timestamp = datetimeformat(recent_results[-1].timestamp) if recent_results else None

    if recent_results:
        # Display the most recent result from the database
        latest_result = recent_results[-1]
        speedtest_result = {
            'download_speed': latest_result.download_speed,
            'upload_speed': latest_result.upload_speed,
            'ping': latest_result.ping
        }
        source = "Database"
        next_test_time = latest_result.timestamp + datetime.timedelta(hours=SPEEDTEST_COOLDOWN_IN_HOURS)
        show_prompt = False
        remaining_time_for_next_test = round((next_test_time - datetime.datetime.now()).total_seconds() / 60)
    else:
        # No recent results, prompt to perform a test
        speedtest_result = None
        source = None
        show_prompt = True
        remaining_time_for_next_test = None
    
    return render_template('dashboard.html', system_info=system_info, 
                           speedtest_result=speedtest_result, 
                           source=source,
                           last_timestamp=last_timestamp,
                           next_test_time=remaining_time_for_next_test, 
                           show_prompt=show_prompt)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Fetch the settings from the database and update them
    settings = DashoardSettings.query.first()
    if settings:
        if request.method == 'POST':
            settings.speedtest_cooldown = int(request.form['speedtest_cooldown'])
            settings.number_of_speedtests = int(request.form['number_of_speedtests'])
            settings.timezone = request.form['timezone']
            db.session.commit()
            flash('Settings updated successfully!', 'success')
        return render_template('settings.html', settings=settings)

@app.route('/speedtest')
def speedtest():
    settings = DashoardSettings.query.first()
    SPEEDTEST_COOLDOWN_IN_HOURS = settings.speedtest_cooldown
    NUMBER_OF_SPEEDTESTS = settings.number_of_speedtests
    n_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=SPEEDTEST_COOLDOWN_IN_HOURS)
    recent_results = SpeedTestResult.query.filter(SpeedTestResult.timestamp > n_hour_ago).all()

    if len(recent_results) < NUMBER_OF_SPEEDTESTS:
        speedtest_result = run_speedtest()
        if speedtest_result['status'] == "Error":
            return render_template('error/speedtest_error.html', error=speedtest_result['message'])

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
        next_test_time = latest_result.timestamp + datetime.timedelta(hours=SPEEDTEST_COOLDOWN_IN_HOURS)
        remaining_time_for_next_test = round((next_test_time - datetime.datetime.now()).total_seconds() / 60)
        return render_template('speedtest_result.html', 
                               speedtest_result=latest_result, 
                               source="Database", 
                               next_test_time=next_test_time,
                               remaining_time_for_next_test=remaining_time_for_next_test)

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
    system_info = get_system_info(SystemInfo=SystemInfo)
    return render_template('system_health.html', system_info=system_info)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
