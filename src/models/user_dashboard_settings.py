
from src.config import db
from src.models.base_model import BaseModel


class UserDashboardSettings(BaseModel):
    """
    User dashboard settings model for the application
    ---
    Properties:
        - id: int
        - user_id: the user id
        - speedtest_cooldown: the cooldown for speedtests
        - number_of_speedtests: the number of speedtests
        - refresh_interval: the refresh interval for the dashboard
    """
    __tablename__ = 'user_dashboard_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    speedtest_cooldown = db.Column(db.Integer, default=30)
    number_of_speedtests = db.Column(db.Integer, default=3)
    refresh_interval = db.Column(db.Integer, default=5)
    bytes_to_megabytes = db.Column(db.Integer, default=1000)
    
