import datetime

from src.config import db

class NetworkSpeedTestResult(db.Model):
    """
    Network speed test result model for the application
    ---
    Properties:
        - id: int
        - download_speed: the download speed
        - upload_speed: the upload speed
        - ping: the ping
        - timestamp: the timestamp of the speed test
    """
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
