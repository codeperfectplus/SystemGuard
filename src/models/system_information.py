import datetime

from src.config import db


class SystemInformation(db.Model):
    __tablename__ = "system_information"
    id = db.Column(db.Integer, primary_key=True)
    cpu_percent = db.Column(db.Float, nullable=False)
    memory_percent = db.Column(db.Float, nullable=False)
    battery_percent = db.Column(db.Float, nullable=False)
    network_sent = db.Column(db.Float, nullable=False)
    network_received = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    