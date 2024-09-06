from src.config import db


class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ping_period = db.Column(db.Integer, nullable=False)  # in seconds
    is_ping = db.Column(db.Boolean, default=True)  # True: ping the site, False: do not ping
    last_status = db.Column(db.String(50), nullable=True)  # Stores 'UP' or 'DOWN'
    last_ping_timestamp = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Website {self.name} - Ping Every {self.ping_period}s>'