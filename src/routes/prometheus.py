from flask import Blueprint, Response, request, render_template, flash, redirect, url_for, jsonify
from prometheus_client import generate_latest
import os
import yaml
import requests
from collections import OrderedDict
from werkzeug.security import check_password_hash

from functools import lru_cache
from flask import g  # 'g' is a request-specific object
from src.config import app, db
from src.models import ExternalMonitornig, UserProfile
from src.utils import ROOT_DIR
from src.routes.helper.common_helper import admin_required
from src.routes.helper.prometheus_helper import (
    load_yaml, 
    save_yaml, 
    is_valid_file, 
    show_targets, 
    prometheus_yml_path,
    update_prometheus_container,
    update_prometheus_config)

# Define the Prometheus Blueprint
prometheus_bp = Blueprint('prometheus', __name__)

# Cache user queries with LRU cache (memory-based, not ideal for distributed apps)
@lru_cache(maxsize=128)
def get_user_by_username(username):
    print('Querying the database...')
    return UserProfile.query.filter_by(username=username).first()

# Verify user login information
def verify_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user.password, password):
        return True
    return False

# Define a route to serve Prometheus metrics
@app.route('/metrics')
def metrics():
    auth = request.authorization
    if not verify_user(auth.username, auth.password):
        return Response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    output = generate_latest()
    output = '\n'.join([line for line in output.decode().split('\n') if not line.startswith('#') and line])
    return Response(output, mimetype='text/plain')

# POST request to manage file paths
@app.route('/external_monitoring', methods=['GET', 'POST'])
@admin_required
def external_monitoring():
    if request.method == 'POST':
        file_path = request.form.get('file_path')

        if not os.path.exists(file_path):
            flash('File path does not exist', 'danger')
            return redirect(url_for('external_monitoring'))

        # Check file path and validity
        if not is_valid_file(file_path):
            flash('Invalid file format. File should have key-value pairs separated by a colon.', 'danger')
            return redirect(url_for('external_monitoring'))

        # Save into the ExternalMonitoring table
        new_task = ExternalMonitornig(file_path=file_path)
        db.session.add(new_task)
        db.session.commit()
        
        return redirect(url_for('external_monitoring'))
    
    data = ExternalMonitornig.query.all()
    return render_template('prometheus/external_monitoring.html', data=data)

# POST request to delete file path
@app.route('/external_monitoring/delete_file_path/<int:id>', methods=['POST'])
@admin_required
def delete_file_path(id):
    file_path = ExternalMonitornig.query.get_or_404(id)
    db.session.delete(file_path)
    db.session.commit()
    flash('File path deleted successfully!', 'success')
    return redirect(url_for('external_monitoring'))

@app.route('/configure_targets')
@admin_required
def configure_targets():
    update_prometheus_config()
    targets_info = show_targets()
    return render_template('other/targets.html', targets_info=targets_info)

@app.route('/targets/restart_prometheus')
@admin_required
def restart_prometheus():
    update_prometheus_container()
    flash('Prometheus container restarted successfully!', 'success')
    return redirect(url_for('configure_targets'))

@app.route('/targets/add_target', methods=['POST'])
def add_target():
    job_name = request.form.get('job_name')
    new_target = request.form.get('new_target')
    username = request.form.get('username')
    password = request.form.get('password')
    scrape_interval = request.form.get('scrape_interval', '15s') + 's'  # New scrape interval
    config = load_yaml(prometheus_yml_path)

    # Validate target format
    if ':' not in new_target:
        flash('Invalid target format. It should be in the format <ip>:<port>.', 'danger')
        return redirect(url_for('configure_targets'))

    job_found = False

    # if job name already exists, add new target to the job
    for scrape_config in config['scrape_configs']:
        if scrape_config['job_name'] == job_name:
            # Append new target
            scrape_config['static_configs'][0]['targets'].append(new_target)
            job_found = True
            
            # Update scrape interval
            scrape_config['scrape_interval'] = scrape_interval
            
            # Prepare the updated job dictionary to maintain order
            updated_job = OrderedDict()
            updated_job['job_name'] = scrape_config['job_name']
            updated_job['static_configs'] = scrape_config['static_configs']
            updated_job['scrape_interval'] = scrape_config['scrape_interval']
            updated_job['basic_auth'] = scrape_config.get('basic_auth', None)

            # Replace the existing job with the updated one
            index = config['scrape_configs'].index(scrape_config)
            config['scrape_configs'][index] = updated_job
            
            break

    if not job_found:
        # Create new job entry
        new_job = OrderedDict()
        new_job['job_name'] = job_name
        new_job['static_configs'] = [{'targets': [new_target]}]
        new_job['scrape_interval'] = scrape_interval
        
        # Add basic_auth if provided
        if username and password:
            new_job['basic_auth'] = {
                'username': username,
                'password': password
            }
        # Append the new job to scrape_configs
        config['scrape_configs'].append(new_job)

    for index, j in enumerate(config['scrape_configs']):
        config['scrape_configs'][index] = OrderedDict(j)

    # Save the updated config
    save_yaml(config, prometheus_yml_path)
    flash('Target added successfully!', 'success')
    # update_prometheus_container()
    return redirect(url_for('configure_targets'))

@app.route('/targets/remove_target', methods=['POST'])
@admin_required
def remove_target():
    job_name = request.form.get('job_name')
    target_to_remove = request.form.get('target_to_remove')
    config = load_yaml(prometheus_yml_path)

    for scrape_config in config['scrape_configs']:
        if scrape_config['job_name'] == job_name:
            targets = scrape_config['static_configs'][0]['targets']
            if target_to_remove in targets:
                targets.remove(target_to_remove)
                flash(f'Target {target_to_remove} removed successfully!', 'success')
                
                # Check if this was the last target, then remove the job
                if not targets:  # If the list is now empty
                    config['scrape_configs'].remove(scrape_config)
                    flash(f'Job {job_name} removed because it had no targets left.', 'success')
            else:
                flash(f'Target {target_to_remove} not found in job {job_name}.', 'warning')
            break
    
    for index, j in enumerate(config['scrape_configs']):
        config['scrape_configs'][index] = OrderedDict(j)

    else:
        flash(f'Job {job_name} not found.', 'warning')

    save_yaml(config, prometheus_yml_path)
    # update_prometheus_container()
    return redirect(url_for('configure_targets'))

@app.route('/targets/change_interval', methods=['POST'])
@admin_required
def change_interval():
    job_name = request.form.get('job_name')
    new_interval = request.form.get('new_interval') + 's'  # New scrape interval
    config = load_yaml(prometheus_yml_path)

    for scrape_config in config['scrape_configs']:
        if scrape_config['job_name'] == job_name:
            scrape_config['scrape_interval'] = new_interval
            flash('Scrape interval updated successfully!', 'success')
            break

    for index, j in enumerate(config['scrape_configs']):
        config['scrape_configs'][index] = OrderedDict(j)
    
    save_yaml(config, prometheus_yml_path)
    # update_prometheus_container()
    return redirect(url_for('configure_targets'))

# change username and password
@app.route('/targets/change_auth', methods=['POST'])
@admin_required
def change_auth():
    job_name = request.form.get('job_name')
    username = request.form.get('username')
    password = request.form.get('password')
    config = load_yaml(prometheus_yml_path)

    found = False
    for scrape_config in config['scrape_configs']:
        if scrape_config['job_name'] == job_name:
            found = True
            scrape_config['basic_auth'] = {
                'username': username,
                'password': password
            }
            flash('Basic Auth updated successfully!', 'success')
            break     
    
    if not found:
        flash(f'Job {job_name} not found.', 'warning')

    for index, j in enumerate(config['scrape_configs']):
        config['scrape_configs'][index] = OrderedDict(j)
    
    save_yaml(config, prometheus_yml_path)
    # update_prometheus_container()
    return redirect(url_for('configure_targets'))

@app.route('/active_alerts')
def active_alerts():
    try:
        response = requests.get('http://localhost:9090/api/v1/alerts')
        alerts_data = response.json()
        alerts = alerts_data['data']['alerts']  # Extract the alerts
    except Exception as e:
        alerts = []
        print(f"Error fetching alerts: {e}")
    
    # Render the alerts in the HTML page
    return render_template('other/active_alerts.html', alerts=alerts)


@app.route('/view_rules')
def view_rules():
    url = "http://localhost:9090/api/v1/rules"
    response = requests.get(url)
    
    if response.status_code == 200:
        rules_data = response.json()
        return render_template('other/view_rules.html', rules=rules_data['data']['groups'])
    else:
        return jsonify({"error": "Unable to fetch rules"}), 500
    

@app.route('/alertmanager/status')
def alertmanager_status():
    url = "http://localhost:9090/api/v1/alertmanagers"
    response = requests.get(url)
    
    if response.status_code == 200:
        alertmanager_data = response.json()
        print(alertmanager_data['data']['activeAlertmanagers'])
        active_alertmanagers = alertmanager_data['data']['activeAlertmanagers']
        return render_template('other/alertmanager_status.html', alertmanagers=active_alertmanagers)
    else:
        return jsonify({"error": "Unable to fetch Alertmanager status"}), 500
    

@app.route('/prometheus/reload')
def reload_prometheus():
    url = "http://localhost:9090/-/reload"  # Ensure this URL is correct
    response = requests.post(url)
    
    # Log response details for debugging
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)

    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Prometheus configuration reloaded."}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to reload Prometheus configuration.", "details": response.text}), response.status_code


@app.route('/prometheus/ready')
def ready_prometheus():
    url = "http://localhost:9090/-/ready"  # Ensure this URL is correct
    response = requests.get(url)
    
    if response.status_code == 200:
        return jsonify({"status": "success", "message": response.text}), 200
    else:
        return jsonify({"status": "error", "message": "Prometheus is not ready.", "details": response.text}), response.status_code
    