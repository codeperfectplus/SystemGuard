from flask_login import UserMixin

from src.config import db

class UserProfile(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_level = db.Column(db.String(10), nullable=False, default='user')
    receive_email_alerts = db.Column(db.Boolean, default=False)
    profession = db.Column(db.String(50), nullable=True)
    
    # Backref renamed to avoid conflict
    dashboard_settings = db.relationship('UserDashboardSettings', backref='user', uselist=False)
    card_settings = db.relationship('UserCardSettings', backref='user', uselist=False)

