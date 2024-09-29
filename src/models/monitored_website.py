from src.config import db
from src.models.base_model import BaseModel


class MonitoredWebsite(BaseModel):
    """
    Monitored website model for the application
    ---
    Properties:
        - id: int
        - name: the name of the website
        - ping_interval: the interval in seconds to ping the website
        - is_ping_active: if the website should be pinged
        - email_address: the email address to send alerts to
        - ping_status: the status of the website
        - ping_status_code: the status code of the website
        - last_ping_time: the last time the website was pinged
        - email_alerts_enabled: if email alerts are enabled
    """
    __tablename__ = 'monitored_websites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ping_interval = db.Column(db.Integer, nullable=False)  # in seconds
    is_ping_active = db.Column(db.Boolean, default=True)  # True: ping the site, False: do not ping
    email_alerts_enabled = db.Column(db.Boolean, default=False)
    email_address = db.Column(db.String(255), nullable=True)
    ping_status = db.Column(db.String(50), nullable=True)  # Stores 'UP' or 'DOWN'
    ping_status_code = db.Column(db.Integer, nullable=True)
    last_ping_time = db.Column(db.DateTime, nullable=True)
    

    def __repr__(self):
        return f'<Website {self.name} - Ping Every {self.ping_interval}s>'