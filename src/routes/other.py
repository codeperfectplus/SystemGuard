import subprocess
from flask import render_template, request, jsonify, flash, blueprints
from flask_login import login_required, current_user

from src.config import app

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

