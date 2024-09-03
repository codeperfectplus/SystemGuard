
from src.config import db

class UserDashboardSettings(db.Model):
    __tablename__ = 'user_dashboard_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    speedtest_cooldown = db.Column(db.Integer, default=3600)
    number_of_speedtests = db.Column(db.Integer, default=1)
    
