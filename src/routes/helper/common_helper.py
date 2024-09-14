from src.models import UserProfile
from src.config import app
from flask_login import current_user
from functools import wraps
from flask import flash, redirect, url_for


def get_email_addresses(user_level=None, receive_email_alerts=True, fetch_all_users=False):
    """Retrieve email addresses of users based on filters."""
    with app.app_context():
        # Build query with filters
        query = UserProfile.query
        if user_level:
            query = query.filter(UserProfile.user_level == user_level)
        if not fetch_all_users:
            query = query.filter(UserProfile.receive_email_alerts == receive_email_alerts)
        
        # Fetch users based on the query
        users = query.all()

        # Return list of email addresses or None if no users found
        return [user.email for user in users] if users else None


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page!", "warning")
            return redirect(url_for("login"))
        if current_user.user_level != "admin":
            flash("You do not have permission to access this page!", "danger")
            return redirect(url_for("settings"))
        return f(*args, **kwargs)
    return wrap

def check_sudo_password(sudo_password):
    """
    Verify the given sudo password by executing a harmless sudo command.
    If the password is correct, it returns True. Otherwise, returns False.

    :param sudo_password: The user's sudo password to validate.
    :return: True if the password is correct, otherwise False.
    """
    try:
        # Test if the sudo password is valid by running a safe sudo command
        result = subprocess.run(
            ['sudo', '-S', 'true'],
            input=f'{sudo_password}\n',
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0
    
    except Exception as e:
        # Log any exception that occurs while validating the sudo password
        return False, str(e)