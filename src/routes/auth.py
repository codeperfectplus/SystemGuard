from flask import Flask, render_template, redirect, url_for, request, blueprints, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from src.config import app, db
from src.models import User

auth_bp = blueprints.Blueprint('auth', __name__)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define the User model

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
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
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
