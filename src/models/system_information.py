import datetime

from src.config import db


class SystemInformation(db.Model):
    """
    System information model for the application
    ---
    Properties:
        - id: int
        - cpu_percent: the CPU percentage
        - memory_percent: the memory percentage
        - battery_percent: the battery percentage
        - network_sent: the network sent
        - network_received: the network received
        - timestamp: the timestamp of the system information
    """
    __tablename__ = "system_information"
    id = db.Column(db.Integer, primary_key=True)
    cpu_percent = db.Column(db.Float, nullable=False)
    memory_percent = db.Column(db.Float, nullable=False)
    battery_percent = db.Column(db.Float, nullable=False)
    network_sent = db.Column(db.Float, nullable=False)
    network_received = db.Column(db.Float, nullable=False)
    dashboard_memory_usage = db.Column(db.Float, nullable=False)
    cpu_frequency = db.Column(db.Float, nullable=False)
    current_temp = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    