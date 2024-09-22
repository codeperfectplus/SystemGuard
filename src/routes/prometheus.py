from flask import Blueprint, Response, request, render_template, flash, redirect, url_for
from prometheus_client import generate_latest
import os
import yaml

from src.config import app, db
from src.models import ExternalMonitornig
from src.utils import ROOT_DIR
from src.routes.helper.prometheus_helper import (
    load_yaml, 
    save_yaml, 
    is_valid_file, 
    show_targets, 
    prometheus_yml_path,
    update_prometheus_container)


# Define the Prometheus Blueprint
prometheus_bp = Blueprint('prometheus', __name__)

# Define a route to serve Prometheus metrics
@app.route('/metrics')
def metrics():
    output = generate_latest()
    output = '\n'.join([line for line in output.decode().split('\n') if not line.startswith('#') and line])
    return Response(output, mimetype='text/plain')

# POST request to manage file paths
@app.route('/external_monitoring', methods=['GET', 'POST'])
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
def delete_file_path(id):
    file_path = ExternalMonitornig.query.get_or_404(id)
    db.session.delete(file_path)
    db.session.commit()
    flash('File path deleted successfully!', 'success')
    return redirect(url_for('external_monitoring'))

@app.route('/targets')
def targets():
    targets_info = show_targets()
    return render_template('other/targets.html', targets_info=targets_info)


@app.route('/targets/add_target', methods=['POST'])
def add_target():
    job_name = request.form.get('job_name')
    new_target = request.form.get('new_target')
    scrape_interval = request.form.get('scrape_interval', '15s') + 's'  # New scrape interval
    config = load_yaml(prometheus_yml_path)

    for scrape_config in config['scrape_configs']:
        if scrape_config['job_name'] == job_name:
            scrape_config['static_configs'][0]['targets'].append(new_target)
            break
    else:
        new_job = {
            'job_name': job_name,
            'static_configs': [{'targets': [new_target]}],
            'scrape_interval': scrape_interval  # Set the specific interval
        }
        config['scrape_configs'].append(new_job)
        
    update_prometheus_container()
    save_yaml(config, prometheus_yml_path)
    flash('Target added successfully!', 'success')
    return redirect(url_for('targets'))

@app.route('/targets/remove_target', methods=['POST'])
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
                
                update_prometheus_container()
                # Check if this was the last target, then remove the job
                if not targets:  # If the list is now empty
                    config['scrape_configs'].remove(scrape_config)
                    flash(f'Job {job_name} removed because it had no targets left.', 'success')
            else:
                flash(f'Target {target_to_remove} not found in job {job_name}.', 'warning')
            break
    else:
        flash(f'Job {job_name} not found.', 'warning')

    save_yaml(config, prometheus_yml_path)
    return redirect(url_for('targets'))

@app.route('/targets/change_interval', methods=['POST'])
def change_interval():
    job_name = request.form.get('job_name')
    new_interval = request.form.get('new_interval') + 's'  # New scrape interval
    config = load_yaml(prometheus_yml_path)

    for scrape_config in config['scrape_configs']:
        if scrape_config['job_name'] == job_name:
            scrape_config['scrape_interval'] = new_interval
            flash('Scrape interval updated successfully!', 'success')
            update_prometheus_container()
            break

    save_yaml(config, prometheus_yml_path)
    return redirect(url_for('targets'))
