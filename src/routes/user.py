import datetime
from flask import render_template, redirect, url_for, request, blueprints, flash, blueprints
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash

from src.config import app, db
from src.models import User
from src.utils import render_template_from_file
from src.scripts.email_me import send_smpt_email
from src.routes.helper import get_email_addresses

user_bp = blueprints.Blueprint('user', __name__)

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.user_level != 'admin':
        flash("Your account does not have permission to view this page.", "danger")
        return render_template("error/permission_denied.html")
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_level = request.form.get('user_level', 'user')
        receive_email_alerts = request.form.get('receive_email_alerts', 'on') == 'on'

        # Check if user already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('add_user'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            user_level=user_level,
            receive_email_alerts=receive_email_alerts
        )

        admin_email_address = get_email_addresses(user_level='admin', receive_email_alerts=True)
        if admin_email_address:
            subject = "New User Alert"
            context = {
                "current_user": current_user.username,
                "username": new_user.username,
                "email": new_user.email,
                "signup_time": datetime.datetime.now(),
                "user_level": new_user.user_level
            }
            html_body = render_template_from_file("src/templates/email_templates/new_user_create.html", **context)
            send_smpt_email(admin_email_address, subject, html_body, is_html=True)

        subject = "Welcome to the systemGuard"  
        context = {
            "username": new_user.username,
            "email": new_user.email,
        }
        html_body = render_template_from_file("src/templates/email_templates/welcome.html", **context)
        send_smpt_email(email, subject, html_body, is_html=True)
            
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('view_users'))

    return render_template('add_user.html')


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

    # Get Admin Emails with Alerts Enabled:
    admin_email_address = get_email_addresses(user_level='admin', receive_email_alerts=True)
    if admin_email_address:
        subject = "User Deletion Alert"
        context = {
            "username": user.username,
            "deletion_time": datetime.datetime.now(),
            "current_user": current_user.username,
        }
        html_body = render_template_from_file("src/templates/email_templates/deletion_email.html", **context)
        send_smpt_email(admin_email_address, subject, html_body, is_html=True)

    db.session.delete(user)
    db.session.commit()

            
    
    flash(f'User {username} has been deleted successfully!', 'success')
    return redirect(url_for('view_users'))
