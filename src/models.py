
from src.config import db
import datetime


class SpeedTestResult(db.Model):
    __tablename__ = 'SpeedTestResult'
    id = db.Column(db.Integer, primary_key=True)
    download_speed = db.Column(db.String(50))
    upload_speed = db.Column(db.String(50))
    ping = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f'<SpeedTestResult {self.download_speed}, {self.upload_speed}, {self.ping}>'


class DashoardSettings(db.Model):
    __tablename__ = 'DashboardSettings'
    id = db.Column(db.Integer, primary_key=True)
    speedtest_cooldown = db.Column(db.Integer, default=1)
    number_of_speedtests = db.Column(db.Integer, default=1)
    timezone = db.Column(db.String(50), default='Asia/Kolkata')

    def __repr__(self):
        return f'<DashboardSettings {self.speedtest_cooldown}, {self.timezone}, {self.number_of_speedtests}>'


class SystemInfo(db.Model):
    __tablename__ = 'SystemInfo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    cpu_percent = db.Column(db.Float)
    memory_percent = db.Column(db.Float)
    disk_usage = db.Column(db.Float)
    battery_percent = db.Column(db.Float)
    cpu_core = db.Column(db.Integer)
    boot_time = db.Column(db.String(50))
    network_sent = db.Column(db.Float)
    network_received = db.Column(db.Float)
    process_count = db.Column(db.Integer)
    swap_memory = db.Column(db.Float)
    uptime = db.Column(db.String(50))
    ipv4_connections = db.Column(db.String(50))
    dashboard_memory_usage = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f'<SystemInfo {self.username}, {self.cpu_percent}, {self.memory_percent}, {self.disk_usage}, {self.battery_percent}, {self.cpu_core}, {self.boot_time}, {self.network_sent}, {self.network_received}, {self.process_count}, {self.swap_memory}, {self.uptime}, {self.ipv4_connections}, {self.ipv6_connections}, {self.dashboard_memory_usage}>'
