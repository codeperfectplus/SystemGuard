import datetime
from flask import Flask, render_template, redirect, url_for, request, blueprints, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


from flask import Flask, render_template, request, jsonify
import subprocess

from src.scripts.email_me import send_email

from src.config import app, db
from src.models import User, SmptEamilPasswordConfig, DashboardSettings
from src.utils import render_template_from_file

auth_bp = blueprints.Blueprint('auth', __name__)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define the User model

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_email_addresses(user_level=None, receive_email_alerts=True, fetch_all_users=False):
    with app.app_context():
        # Build query filter based on the presence of `user_level`
        filters = []
        if user_level:
            filters.append(User.user_level == user_level)
        if not fetch_all_users:
            filters.append(User.receive_email_alerts == receive_email_alerts)
        
        # Query the database with the constructed filters
        users = User.query.filter(*filters).all()
        
        # Check if no users were found
        if not users:
            return None

        # Return list of email addresses
        return [user.email for user in users]

# Get Admin Emails with Alerts Enabled:
# admin_emails = get_email_addresses(user_level='admin', receive_email_alerts=True)
# Get All Admin Emails Regardless of Alert Preference:
# all_admin_emails = get_email_addresses(user_level='admin', fetch_all_users=True)

# Get All Users with Alerts Enabled:
# all_user_emails = get_email_addresses(receive_email_alerts=True)
# Get All Users Regardless of Alert Preference:
# all_users_emails = get_email_addresses(fetch_all_users=True)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            receiver_email = current_user.email
            admin_email_address = get_email_addresses(user_level='admin', receive_email_alerts=True)
            # if receiver_email in admin_email_address don't send email to the admin
            # log in alert to admin

            if admin_email_address:
                context = {"username": current_user.username, "login_time": datetime.datetime.now()}
                login_body = render_template_from_file("src/templates/email_templates/admin_login_alert.html", **context)
                # send_email(admin_email_address, 'Login Alert', login_body, is_html=True)

            # log in alert to user
            if receiver_email:
                context = {"username": current_user.username, "login_time": datetime.datetime.now()}
                login_body = render_template_from_file("src/templates/email_templates/login.html", **context)
                # send_email(receiver_email, 'Login Alert', login_body, is_html=True)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    receiver_email = current_user.email
    if receiver_email:
        context = {"username": current_user.username}
        logout_body = render_template_from_file("src/templates/email_templates/logout.html", **context)
        # send_email(receiver_email, 'Logout Alert', logout_body, is_html=True)
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        
        # Get Admin Emails with Alerts Enabled:
        admin_email_address = get_email_addresses(user_level='admin', receive_email_alerts=True)
        # extends the signup user to send an email to the admin
        if admin_email_address:
            send_email(admin_email_address, 'New User Alert', f'{username} has signed up to the system.')
        
        # send email to the new user
        send_email([new_user.email], 'Welcome to the system', f'Hello {new_user.username}, welcome to the system.')

        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully, please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/protected')
@login_required
def protected():
    if current_user.user_level == 'admin':
        return f'Hello, Admin {current_user.username}! This is a protected page.'
    return f'Hello, {current_user.username}! This is a protected page.'

@app.route('/users')
@login_required
def view_users():
    if current_user.user_level != 'admin':
        flash("Your account does not have permission to view this page.", "danger")
        return render_template("error/permission_denied.html")

    # Fetch all users from the database
    users = User.query.all()

    return render_template('view_users.html', users=users)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def change_user_settings(username):
    user = User.query.filter_by(username=username).first_or_404()

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_user_level = request.form['user_level']
        receive_email_alerts = 'receive_email_alerts' in request.form

        # Update user details
        user.username = new_username
        user.email = new_email
        user.user_level = new_user_level
        user.receive_email_alerts = receive_email_alerts

        db.session.commit()

        flash('User settings updated successfully!', 'success')
        return redirect(url_for('change_user_settings', username=user.username))

    return render_template('change_user.html', user=user)

@app.route('/delete_user/<username>', methods=['POST'])
@login_required
def delete_user(username):
    if current_user.user_level != 'admin':
        flash("Your account does not have permission to perform this action.", "danger")
        return redirect(url_for('view_users'))  # Redirect to the users page

    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} has been deleted successfully!', 'success')
    return redirect(url_for('view_users'))

@app.route("/update-email-password", methods=["GET", "POST"])
@login_required
def update_smpt_email_password():
    smtp_config = SmptEamilPasswordConfig.query.first()

    if request.method == "POST":
        new_email = request.form.get("email")
        new_password = request.form.get("password")

        if not new_email or not new_password:
            flash("Please provide email and password.", "danger")
            return redirect(url_for("update_smpt_email_password"))
        
        
        if not smtp_config:
            smtp_config = SmptEamilPasswordConfig(email=new_email, password=new_password)
            db.session.add(smtp_config)
        else:
            smtp_config.email = new_email
            smtp_config.password = new_password        
        
        db.session.commit()
        flash("Email and password updated successfully!", "success")
        return redirect(url_for("update_smpt_email_password"))

    return render_template("update_smpt_email_password.html", smtp_config=smtp_config)

@app.route("/send_email", methods=["GET", "POST"])
@login_required
def send_email_page():
    dasboard_settings = DashboardSettings.query.first()
    receiver_email = get_email_addresses(user_level='admin', receive_email_alerts=True)    
    if dasboard_settings:
        enable_alerts = dasboard_settings.enable_alerts
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
            respose = send_email(receiver_email, subject, body, attachment_path)
            print(respose)
            if respose and respose.get("status") == "success":
                flash(respose.get("message"), "success")
        except Exception as e:
            flash(f"Failed to send email: {str(e)}", "danger")
        
        return redirect(url_for('send_email_page'))

    return render_template("send_email.html", enable_alerts=enable_alerts)

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

if __name__ == '__main__':
    app.run(debug=True)
