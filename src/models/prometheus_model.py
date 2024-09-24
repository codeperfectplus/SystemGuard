from src.config import db


class ExternalMonitornig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
