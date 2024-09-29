from flask_login import UserMixin
from werkzeug.security import check_password_hash


from src.config import db
from src.models.base_model import BaseModel


class UserProfile(BaseModel, UserMixin):
    """
    User profile model for the application
    ---
    Properties:
        - id: int
        - username: the username
        - email: the email
        - password: the password
        - user_level: the user level
        - receive_email_alerts: if the user receives email alerts
        - profession: the profession of the user
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_level = db.Column(db.String(10), nullable=False, default='user')
    receive_email_alerts = db.Column(db.Boolean, default=False)
    profession = db.Column(db.String(50), nullable=True)
    
    # Backref renamed to avoid conflict
    dashboard_settings = db.relationship('UserDashboardSettings', backref='user', uselist=False)
    card_settings = db.relationship('UserCardSettings', backref='user', uselist=False)

    def __repr__(self):
        return f"<UserProfile {self.username}>"
    
    @staticmethod
    def get_by_username(username):
        return UserProfile.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email):
        return UserProfile.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_id(id):
        return UserProfile.query.get(id)
    
    @staticmethod
    def get_all():
        return UserProfile.query.all()
    
    # check_hashed_password
    def check_password(self, password):
        return check_password_hash(self.password, password)