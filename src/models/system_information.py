import datetime

from src.config import db


class SystemInformation(db.Model):
    __tablename__ = "system_information"
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
    cpu_frequency = db.Column(db.String(50))
    current_temp = db.Column(db.String(50))

    def __repr__(self):
        return f"<SystemInfo {self.username}, {self.cpu_percent}, {self.memory_percent}, {self.disk_usage}, {self.battery_percent}, {self.cpu_core}, {self.boot_time}, {self.network_sent}, {self.network_received}, {self.process_count}, {self.swap_memory}, {self.uptime}, {self.ipv4_connections}, {self.ipv6_connections}, {self.dashboard_memory_usage}>"
