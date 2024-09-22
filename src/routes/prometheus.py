from flask import Blueprint, Response, request, render_template, flash, redirect, url_for
from prometheus_client import generate_latest
import os

from src.config import app, db
from src.models import ExternalMonitornig

# Define the Prometheus Blueprint
prometheus_bp = Blueprint('prometheus', __name__)


def is_valid_file(file_path: str) -> bool:
    """Checks if a file is valid and have key-value pairs separated by a colon."""
    with open(file_path, 'r') as file:
        for line in file:
            if not line.strip():
                continue

            if ':' not in line:
                return False

    return True

# Define a route to serve Prometheus metrics
@app.route('/metrics')
def metrics():
    output = generate_latest()
    output = '\n'.join([line for line in output.decode().split('\n') if not line.startswith('#') and line])
    return Response(output, mimetype='text/plain')

# post request to add file path
@app.route('/prometheus/external_monitoring', methods=['GET', 'POST'])
def external_monitoring():
    if request.method == 'POST':
        
        file_path = request.form.get('file_path')

        if not os.path.exists(file_path):
            flash('File path does not exist', 'danger')
            return redirect(url_for('external_monitoring'))
        
        # check file path and is_valid
        if not is_valid_file(file_path):
            flash('Invalid file format. File should have key-value pairs separated by a colon.', 'danger')
            return redirect(url_for('external_monitoring'))
        
        # save into the ExternalMonitornig table
        new_task = ExternalMonitornig(file_path=file_path)
        # commit the changes
        db.session.add(new_task)
        db.session.commit()
        
        # read_file_and_update_metric(file_path=file_path)
        return redirect(url_for('external_monitoring'))
    
    data = ExternalMonitornig.query.all()
    return render_template('prometheus/external_monitoring.html',  data=data)


# post request to delete file path
@app.route('/prometheus/delete_file_path/<int:id>', methods=['POST'])
def delete_file_path(id):
    file_path = ExternalMonitornig.query.get_or_404(id)
    db.session.delete(file_path)
    db.session.commit()
    flash('File path deleted successfully!', 'success')
    return redirect(url_for('external_monitoring'))
