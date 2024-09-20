from flask import Blueprint, Response, request, jsonify, render_template, flash, redirect, url_for
from prometheus_client import generate_latest

from src.config import app, db
from src.models import ExternalMonitornig


# Define the Prometheus Blueprint
prometheus_bp = Blueprint('prometheus', __name__)

# Define a route to serve Prometheus metrics
@app.route('/metrics')
def metrics():
    output = generate_latest()
    output = '\n'.join([line for line in output.decode().split('\n') if not line.startswith('#') and line])
    return Response(output, mimetype='text/plain')

# post request to add file path
@app.route('/prometheus/add_file_path', methods=['GET', 'POST'])
def add_file_path():
    if request.method == 'POST':
        
        file_path = request.form.get('file_path')
        # save into the ExternalMonitornig table
        new_task = ExternalMonitornig(file_path=file_path)
        # commit the changes
        db.session.add(new_task)
        db.session.commit()
        
        # read_file_and_update_metric(file_path=file_path)
        return redirect(url_for('add_file_path'))
    
    data = ExternalMonitornig.query.all()
    return render_template('prometheus/add_file_path.html',  data=data)


# post request to delete file path
@app.route('/prometheus/delete_file_path/<int:id>', methods=['POST'])
def delete_file_path(id):
    file_path = ExternalMonitornig.query.get_or_404(id)
    db.session.delete(file_path)
    db.session.commit()
    flash('File path deleted successfully!', 'success')
    return redirect(url_for('add_file_path'))

