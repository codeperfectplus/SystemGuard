from src.config import db


class MonitoredWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ping_interval = db.Column(db.Integer, nullable=False)  # in seconds
    is_ping_active = db.Column(db.Boolean, default=True)  # True: ping the site, False: do not ping
    ping_status = db.Column(db.String(50), nullable=True)  # Stores 'UP' or 'DOWN'
    ping_status_code = db.Column(db.Integer, nullable=True)
    last_ping_time = db.Column(db.DateTime, nullable=True)
    email_alerts_enabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Website {self.name} - Ping Every {self.ping_interval}s>'