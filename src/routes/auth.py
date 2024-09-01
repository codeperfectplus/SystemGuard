from flask import Flask, render_template, redirect, url_for, request, blueprints, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from src.scripts.email_me import send_email

from src.config import app, db
from src.models import User, EmailPassword

auth_bp = blueprints.Blueprint('auth', __name__)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define the User model

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_admin_emails_for_email_alerts():
    with app.app_context():
        admin_emails = User.query.filter_by(user_level='admin', receive_email_alerts=True).all()
        print(admin_emails)
        if not admin_emails:
            return None
        return [admin.email for admin in admin_emails]
    
def get_all_users_emails(receive_email_alerts=True):
    with app.app_context():
        users = User.query.filter_by(receive_email_alerts=receive_email_alerts).all()
        if not users:
            return None
        return [user.email for user in users]



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            admin_email_address = get_admin_emails_for_email_alerts()
            if admin_email_address:
                send_email(admin_email_address, 'Login Alert', f'{user.username} logged in to the system.')
            
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

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
        
        admin_email_address = get_admin_emails_for_email_alerts()
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# def admin_required(f):
#     """Decorator to ensure the current user is an admin."""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.user_level != 'admin':
#             flash('Access denied. Admins only.')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# def user_required(f):
#     """Decorator to ensure the current user is a regular user."""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.user_level != 'user':
#             flash('Access denied. Users only.')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

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
def update_email_password():
    email_password = EmailPassword.query.first()

    if request.method == "POST":
        new_email = request.form.get("email")
        new_password = request.form.get("password")

        if new_email:
            email_password.email = new_email
        if new_password:
            email_password.password = new_password

        db.session.commit()
        flash("Email and password updated successfully!", "success")
        return redirect(url_for("update_email_password"))

    return render_template("update_email_password.html", email_password=email_password)

@app.route("/send_email", methods=["GET", "POST"])
@login_required
def send_email_page():
    if request.method == "POST":
 
        receiver_email = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")
        attachment = request.files.get("attachment")

        if not receiver_email or not subject or not body:
            flash("Please provide recipient, subject, and body.", "danger")
            return redirect(url_for('send_email_page'))
        
        if receiver_email == "all_users":
            receiver_email = get_all_users_emails()
        elif receiver_email == "admin_users":
            receiver_email = get_admin_emails_for_email_alerts()

        if not receiver_email:
            flash("No users found to send email to.", "danger")
            return redirect(url_for('send_email_page'))
        
        # Save attachment if any
        attachment_path = None
        if attachment:
            attachment_path = f"/tmp/{attachment.filename}"
            attachment.save(attachment_path)
        try:
            send_email(receiver_email, subject, body, attachment_path)
            flash("Email sent successfully!", "success")
        except Exception as e:
            flash(f"Failed to send email: {str(e)}", "danger")
        
        return redirect(url_for('send_email_page'))

    return render_template("send_email.html")