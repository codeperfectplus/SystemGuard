from src.config import db

class SMTPSettings(db.Model):
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
