import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src.config import db, app


class SpeedTestResult(db.Model):
    __tablename__ = "SpeedTestResult"
    id = db.Column(db.Integer, primary_key=True)
    download_speed = db.Column(db.String(50))
    upload_speed = db.Column(db.String(50))
    ping = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return (
            f"<SpeedTestResult {self.download_speed}, {self.upload_speed}, {self.ping}>"
        )

class DashboardSettings(db.Model):
    __tablename__ = "DashboardSettings"
    id = db.Column(db.Integer, primary_key=True)
    
    # speedtest setting
    speedtest_cooldown = db.Column(db.Integer, default=1)
    number_of_speedtests = db.Column(db.Integer, default=1)

    # general settings
    timezone = db.Column(db.String(50), default="Asia/Kolkata")
    enable_cache = db.Column(db.Boolean, default=True)
    enable_alerts = db.Column(db.Boolean, default=False)

    # page enable/disable
    is_cpu_info_enabled = db.Column(db.Boolean, default=True)
    is_memory_info_enabled = db.Column(db.Boolean, default=True)
    is_disk_info_enabled = db.Column(db.Boolean, default=True)
    is_network_info_enabled = db.Column(db.Boolean, default=True)
    is_process_info_enabled = db.Column(db.Boolean, default=False)


    # card enable/disable
    is_user_card_enabled = db.Column(db.Boolean, default=True)
    is_server_card_enabled = db.Column(db.Boolean, default=True)
    is_battery_card_enabled = db.Column(db.Boolean, default=True)
    is_cpu_core_card_enabled = db.Column(db.Boolean, default=True)
    is_cpu_usage_card_enabled = db.Column(db.Boolean, default=True)
    is_cpu_temp_card_enabled = db.Column(db.Boolean, default=True)
    is_dashboard_memory_card_enabled = db.Column(db.Boolean, default=True)
    is_memory_usage_card_enabled = db.Column(db.Boolean, default=True)
    is_disk_usage_card_enabled = db.Column(db.Boolean, default=True)
    is_system_uptime_card_enabled = db.Column(db.Boolean, default=True)
    is_network_statistic_card_enabled = db.Column(db.Boolean, default=True)
    is_speedtest_enabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<DashboardSettings {self.speedtest_cooldown}, {self.timezone}, {self.number_of_speedtests}>"


class SystemInfo(db.Model):
    __tablename__ = "SystemInfo"
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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    user_level = db.Column(db.String(50), nullable=False, default='user')
    receive_email_alerts = db.Column(db.Boolean, default=True)


class SmptEamilPasswordConfig(db.Model):
    __tablename__ = "SmptEamilPasswordConfig"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


with app.app_context():
    print("Creating tables")
    db.create_all()

    # Initialize default settings
    settings = DashboardSettings.query.first()
    if not settings:
        db.session.add(DashboardSettings())
        db.session.commit()

    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('adminpassword')
        admin_user = User(username='admin', email="codeperfectplus@gmail.com", password=hashed_password, user_level='admin',
                          receive_email_alerts=True)
        
        db.session.add(admin_user)
        db.session.commit()

    # create a user if not exists
    if not User.query.filter_by(username='user').first():
        hashed_password = generate_password_hash('userpassword')
        user = User(username='user', email="test@mail.com",
                    password=hashed_password, user_level='user', receive_email_alerts=False)
        
        db.session.add(user)
        db.session.commit()

# ibject for all templates
@app.context_processor
def inject_settings():
    settings = DashboardSettings.query.first()
    return dict(settings=settings)

