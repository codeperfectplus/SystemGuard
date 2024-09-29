import os
import datetime
from flask import render_template, redirect, url_for, request, blueprints, flash, blueprints
from flask_login import current_user
from werkzeug.security import generate_password_hash

from src.config import app, db
from src.models import UserProfile, UserDashboardSettings, UserCardSettings, PageToggleSettings
from src.utils import render_template_from_file, ROOT_DIR
from src.alert_manager import send_smtp_email
from src.routes.helper.common_helper import get_email_addresses
from src.config import get_app_info
from src.routes.helper.common_helper import admin_required

user_management_bp = blueprints.Blueprint('user_management', __name__)

@app.route('/create_user', methods=['GET', 'POST'])
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        profession = request.form['profession']
        user_level = request.form.get('user_level', 'user')
        receive_email_alerts = request.form.get('receive_email_alerts', 'on') == 'on'

        # Check if user already exists
        if UserProfile.query.filter_by(username=username).first() or UserProfile.query.filter_by(email=email).first():
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('create_user'))

        new_user = UserProfile(
            username=username,
            email=email,
            password=generate_password_hash(password),
            profession=profession,
            user_level=user_level,
            receive_email_alerts=receive_email_alerts
        )

        # Send email alerts to admins
        admin_email_address = get_email_addresses(user_level='admin', receive_email_alerts=True)
        if admin_email_address:
            subject = "New User Alert"
            context = {
                "current_user": current_user.username,
                "username": new_user.username,
                "email": new_user.email,
                "registration_time": datetime.datetime.now(),
                "user_level": new_user.user_level
            }
            new_user_alert_template =  os.path.join(ROOT_DIR, "src/templates/email_templates/new_user_create.html")
            email_body = render_template_from_file(new_user_alert_template, **context)
            send_smtp_email(admin_email_address, subject, email_body, is_html=True)

        # Send welcome email to new user
        subject = f"Welcome to the {get_app_info()['title']}"  
        context = {
            "username": new_user.username,
            "email": new_user.email,
        }
        welcome_email_template = os.path.join(ROOT_DIR, "src/templates/email_templates/welcome.html")
        email_body = render_template_from_file(welcome_email_template, **context)
        send_smtp_email(email, subject, email_body, is_html=True)

        # Add and commit the new user to get the correct user ID
        db.session.add(new_user)
        db.session.commit()  # Commit to generate the ID
        
        # Now you can use the new user's ID to create related settings
        db.session.add(UserDashboardSettings(user_id=new_user.id))
        db.session.add(UserCardSettings(user_id=new_user.id))
        db.session.add(PageToggleSettings(user_id=new_user.id))
        db.session.commit()

        flash('User created successfully!', 'success')
        return redirect(url_for('view_users'))

    return render_template('users/create_user.html')

@app.route('/users')
@admin_required
def view_users():
    users = UserProfile.query.all()
    return render_template('users/view_users.html', users=users)

@app.route('/user/<username>', methods=['GET', 'POST'])
@admin_required
def change_user_settings(username):
    user = UserProfile.query.filter_by(username=username).first_or_404()

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_user_level = request.form['user_level']
        new_profession = request.form['profession']
        receive_email_alerts = 'receive_email_alerts' in request.form

        # Update user details
        user.username = new_username
        user.email = new_email
        user.user_level = new_user_level
        user.receive_email_alerts = receive_email_alerts
        user.profession = new_profession

        db.session.commit()

        flash('User settings updated successfully!', 'success')
        return redirect(url_for('view_users', username=user.username))

    return render_template('users/change_user.html', user=user)

@app.route('/delete_user/<username>', methods=['POST'])
@admin_required
def delete_user(username):
    user = UserProfile.query.filter_by(username=username).first_or_404()
    # Get Admin Emails with Alerts Enabled:
    admin_email_address = get_email_addresses(user_level='admin', receive_email_alerts=True)
    if admin_email_address:
        subject = "User Deletion Alert"
        context = {
            "username": user.username,
            "deletion_time": datetime.datetime.now(),
            "current_user": current_user.username,
        }
        deletion_email_template = os.path.join(ROOT_DIR, "src/templates/email_templates/deletion_email.html")
        email_body = render_template_from_file(deletion_email_template, **context)
        send_smtp_email(admin_email_address, subject, email_body, is_html=True)

    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} has been deleted successfully!', 'success')
    return redirect(url_for('view_users'))

