import datetime
import subprocess
from flask import render_template, request, jsonify, flash, blueprints, redirect, url_for
from flask_login import login_required, current_user

from src.models import UserCardSettings, UserDashboardSettings, ApplicationGeneralSettings
from src.config import app, db
from src.routes.helper import get_email_addresses
from src.scripts.email_me import send_smpt_email


other_bp = blueprints.Blueprint('other', __name__)

@app.route('/terminal', methods=['GET', 'POST'])
@login_required
def terminal():
    if current_user.user_level != 'admin':
        flash("Your account does not have permission to view this page.", "danger")
        return render_template("error/403.html")
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

    try:
        # Query the settings for the current user
        settings = UserDashboardSettings.query.filter_by(user_id=user_id).first()

        # If settings do not exist for the user, create them
        if not settings:
            settings = UserDashboardSettings(user_id=user_id, refresh_interval=new_interval)
            db.session.add(settings)
        else:
            # Update the refresh interval
            settings.refresh_interval = new_interval

        # Commit changes to the database
        db.session.commit()

        return jsonify({'success': 'Refresh interval updated successfully', 'refresh_interval': new_interval})

    except Exception as e:
        # Handle any exceptions that occur during database operations
        db.session.rollback()  # Rollback any changes if an error occurs
        return jsonify({'error': 'An error occurred while updating the refresh interval', 'details': str(e)}), 500


@app.route("/send_email", methods=["GET", "POST"])
@login_required
def send_email_page():
    if current_user.user_level != 'admin':
        flash("Your account does not have permission to view this page.", "danger")
        flash("User level for this account is: " + current_user.user_level, "danger")
        flash("Please contact your administrator for more information.", "danger")
        return render_template("error/403.html")
    receiver_email = get_email_addresses(user_level='admin', receive_email_alerts=True)    
    general_settings = ApplicationGeneralSettings.query.first()
    if general_settings:
        enable_alerts = general_settings.enable_alerts
    if request.method == "POST":
        receiver_email = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")
        priority = request.form.get("priority")
        attachment = request.files.get("attachment")

        if not receiver_email or not subject or not body:
            flash("Please provide recipient, subject, and body.", "danger")
            return redirect(url_for('send_email_page'))
        
        print("Priority:", priority)
        print("receiver_email:", receiver_email)

        # on high priority, send to all users or admin users even the receive_email_alerts is False
        if priority == "high" and receiver_email == "all_users":
            print("Sending to all users")
            receiver_email = get_email_addresses(fetch_all_users=True)
        elif priority == "high" and receiver_email == "admin_users":
            print("Sending to admin users")
            receiver_email = get_email_addresses(user_level='admin', fetch_all_users=True)

        # priority is low, send to users with receive_email_alerts is True
        if priority == "low" and receiver_email == "all_users":
            print("Sending to all users with receive_email_alerts=True")
            receiver_email = get_email_addresses(receive_email_alerts=True)
        elif priority == "low" and receiver_email == "admin_users":
            print("Sending to admin users with receive_email_alerts=True")
            receiver_email = get_email_addresses(user_level='admin', receive_email_alerts=True)

        if not receiver_email:
            flash("No users found to send email to.", "danger")
            return redirect(url_for('send_email_page'))
        
        # Save attachment if any
        attachment_path = None
        if attachment:
            attachment_path = f"/tmp/{attachment.filename}"
            attachment.save(attachment_path)
        try:
            respose = send_smpt_email(receiver_email, subject, body, attachment_path)
            print(respose)
            if respose and respose.get("status") == "success":
                flash(respose.get("message"), "success")
        except Exception as e:
            flash(f"Failed to send email: {str(e)}", "danger")
        
        return redirect(url_for('send_email_page'))

    return render_template("other/send_email.html", enable_alerts=enable_alerts)
