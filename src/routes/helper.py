from src.models import UserProfile
from src.config import app


def get_email_addresses(user_level=None, receive_email_alerts=True, fetch_all_users=False):
    with app.app_context():
        # Build query filter based on the presence of `user_level`
        filters = []
        if user_level:
            filters.append(UserProfile.user_level == user_level)
        if not fetch_all_users:
            filters.append(UserProfile.receive_email_alerts == receive_email_alerts)
        
        # Query the database with the constructed filters
        users = UserProfile.query.filter(*filters).all()
        
        # Check if no users were found
        if not users:
            return None

        # Return list of email addresses
        return [user.email for user in users]