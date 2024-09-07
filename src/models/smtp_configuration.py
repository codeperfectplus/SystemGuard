from src.config import db

class SMTPSettings(db.Model):
    __tablename__ = "smtp_settings"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    smtp_server = db.Column(db.String(150), nullable=False)
    smtp_port = db.Column(db.Integer, nullable=False)
    email_from = db.Column(db.String(150), nullable=False)
