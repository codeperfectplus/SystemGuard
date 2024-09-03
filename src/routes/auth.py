import datetime
from flask import render_template, redirect, url_for, request, blueprints, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.scripts.email_me import send_smpt_email
from src.config import app, db
from src.models import User, DashboardSettings
from src.utils import render_template_from_file
from src.routes.helper import get_email_addresses

auth_bp = blueprints.Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
                if receiver_email in admin_email_address:
                    admin_email_address.remove(receiver_email)
                if admin_email_address:
                    context = {"username": current_user.username, "login_time": datetime.datetime.now()}
                    login_body = render_template_from_file("src/templates/email_templates/admin_login_alert.html", **context)
                    send_smpt_email(admin_email_address, 'Login Alert', login_body, is_html=True)

            # log in alert to user
            if receiver_email:
                context = {"username": current_user.username, "login_time": datetime.datetime.now()}
                login_body = render_template_from_file("src/templates/email_templates/login.html", **context)
                send_smpt_email(receiver_email, 'Login Alert', login_body, is_html=True)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    receiver_email = current_user.email
    if receiver_email:
        context = {"username": current_user.username}
        logout_body = render_template_from_file("src/templates/email_templates/logout.html", **context)
        send_smpt_email(receiver_email, 'Logout Alert', logout_body, is_html=True)
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_level = request.form.get('user_level', 'user')  # Default to 'user' if not provided
        receive_email_alerts = 'receive_email_alerts' in request.form  # Checkbox is either checked or not
        profession = request.form.get('profession', None)

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, 
                        email=email, 
                        password=hashed_password, 
                        user_level=user_level, 
                        receive_email_alerts=receive_email_alerts,
                        profession=profession)
        
        # Get Admin Emails with Alerts Enabled:
        admin_email_address = get_email_addresses(user_level='admin', receive_email_alerts=True)
        if admin_email_address:
            subject = "New User Alert"
            context = {
                "username": new_user.username,
                "email": new_user.email,
                "signup_time": datetime.datetime.now(),
                "user_level": new_user.user_level
            }
            html_body = render_template_from_file("src/templates/email_templates/new_user_alert.html", **context)
            send_smpt_email(admin_email_address, subject, html_body, is_html=True)
            
        # Send email to the new user
        subject = "Welcome to the systemGuard"  
        context = {
            "username": new_user.username,
            "email": new_user.email,
        }
        html_body = render_template_from_file("src/templates/email_templates/welcome.html", **context)
        send_smpt_email(email, subject, html_body, is_html=True)

        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully, please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

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
            respose = send_smpt_email(receiver_email, subject, body, attachment_path)
            print(respose)
            if respose and respose.get("status") == "success":
                flash(respose.get("message"), "success")
        except Exception as e:
            flash(f"Failed to send email: {str(e)}", "danger")
        
        return redirect(url_for('send_email_page'))

    return render_template("send_email.html", enable_alerts=enable_alerts)

