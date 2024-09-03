import subprocess
from flask import render_template, request, jsonify, flash, blueprints
from flask_login import login_required, current_user
from src.models import FeatureToggleSettings
from src.config import app, db

other_bp = blueprints.Blueprint('other', __name__)

@app.route('/terminal', methods=['GET', 'POST'])
@login_required
def terminal():
    if current_user.user_level != 'admin':
        flash("Your account does not have permission to view this page.", "danger")
        return render_template("error/permission_denied.html")
    if request.method == 'POST':
        command = request.form.get('command')
        if command:
            try:
                # Run the command and capture the output
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                # If the command fails, capture the error output
                output = e.output
            return jsonify(output=output)
    return render_template('terminal.html')


@app.route('/update-refresh-interval', methods=['POST'])
def update_refresh_interval():
    # Retrieve user ID from session or other authentication methods
    user_id = current_user.id

    # Get the new refresh interval from the request
    new_interval = request.json.get('refresh_interval')

    # Validate the new interval (must be a positive integer)
    if not isinstance(new_interval, int) or new_interval <= 0:
        return jsonify({'error': 'Invalid refresh interval value'}), 400

    # Query the settings for the current user
    settings = FeatureToggleSettings.query.filter_by(user_id=user_id).first()

    # If settings do not exist for the user, create them
    if not settings:
        settings = FeatureToggleSettings(user_id=user_id, refresh_interval=new_interval)
        db.session.add(settings)
    else:
        # Update the refresh interval
        settings.refresh_interval = new_interval

    # Commit changes to the database
    db.session.commit()

    return jsonify({'success': 'Refresh interval updated successfully', 'refresh_interval': new_interval})
