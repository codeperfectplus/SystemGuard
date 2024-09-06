from src.models import UserProfile
from src.config import app

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
