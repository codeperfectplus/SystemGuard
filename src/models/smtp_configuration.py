from src.config import db
from src.models.base_model import BaseModel


class SMTPSettings(BaseModel):
    """
    SMTP settings model for the application
    ---
    Properties:
        - id: int
        - username: the username for the SMTP server
        - password: the password for the SMTP server
        - smtp_server: the SMTP server
        - smtp_port: the SMTP port
        - email_from: the email address to send from
    """
    __tablename__ = "smtp_settings"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    smtp_server = db.Column(db.String(150), nullable=False)
    smtp_port = db.Column(db.Integer, nullable=False)
    email_from = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<SMTPSettings {self.username}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port,
            "email_from": self.email_from
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return SMTPSettings.query.all()
    
    @staticmethod
    def get_by_id(id):
        return SMTPSettings.query.get(id)
    
    @staticmethod
    def get_by_username(username):
        return SMTPSettings.query.filter_by(username=username).first()
