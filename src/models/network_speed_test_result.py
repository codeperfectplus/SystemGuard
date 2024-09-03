import datetime

from src.config import db

class NetworkSpeedTestResult(db.Model):
    __tablename__ = "network_speed_test_result"
    id = db.Column(db.Integer, primary_key=True)
    download_speed = db.Column(db.String(50))
    upload_speed = db.Column(db.String(50))
    ping = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return (
            f"<SpeedTestResult {self.download_speed}, {self.upload_speed}, {self.ping}>"
        )
