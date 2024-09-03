from flask import blueprints
from src.models import User
from src.config import app
from flask_login import LoginManager


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