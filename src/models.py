import json
import datetime
from flask_login import UserMixin, current_user
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

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_level = db.Column(db.String(10), nullable=False, default='user')
    receive_email_alerts = db.Column(db.Boolean, default=False)
    profession = db.Column(db.String(50), nullable=True)
    
    # Backref renamed to avoid conflict
    dashboard_settings = db.relationship('DashboardSettings', backref='user', uselist=False)
    card_settings = db.relationship('CardSettings', backref='user', uselist=False)

class DashboardSettings(db.Model):
    __tablename__ = 'dashboard_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    speedtest_cooldown = db.Column(db.Integer, default=3600)
    number_of_speedtests = db.Column(db.Integer, default=1)
    

class FeatureTogglesSettings(db.Model):
    __tablename__ = 'FeatureToggles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Feature Toggles
    is_cpu_info_enabled = db.Column(db.Boolean, default=True)
    is_memory_info_enabled = db.Column(db.Boolean, default=True)
    is_disk_info_enabled = db.Column(db.Boolean, default=True)
    is_network_info_enabled = db.Column(db.Boolean, default=True)
    is_process_info_enabled = db.Column(db.Boolean, default=True)

class CardSettings(db.Model):
    __tablename__ = 'CardSettings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Card Toggles
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
    is_speedtest_enabled = db.Column(db.Boolean, default=True)
    
class GeneralSettings(db.Model):
    __tablename__ = 'general_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    enable_alerts = db.Column(db.Boolean, default=False)
    timezone = db.Column(db.String(50), default='UTC')
    enable_cache = db.Column(db.Boolean, default=False)


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


# home page to show links to multiple dashbaord
class DashboardNetwork(db.Model):
    __tablename__ = "DashboardGroup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    port = db.Column(db.Integer, nullable=True)
    link = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f"<DashboardGroup {self.name}, {self.description}>"


class SmptEamilPasswordConfig(db.Model):
    __tablename__ = "SmptEamilPasswordConfig"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


with app.app_context():
    print("Creating tables")
    db.create_all()

    # initialize default dashboard settings for users
    users = User.query.all()
    for user in users:
        if not user.dashboard_settings:
            db.session.add(DashboardSettings(user_id=user.id))
            db.session.add(CardSettings(user_id=user.id))
            db.session.add(FeatureTogglesSettings(user_id=user.id))
            db.session.commit()

    pre_defined_users_json = "src/assets/predefine_user.json"
    with open(pre_defined_users_json, "r") as file:
        pre_defined_users = json.load(file)
    for user in pre_defined_users:
        if not User.query.filter_by(user_level=user['user_level']).first():
            hashed_password = generate_password_hash(user['password'])
            user = User(username=user['username'], email=user['email'], password=hashed_password, user_level=user['user_level'],
                        receive_email_alerts=user['receive_email_alerts'], profession=user['profession'])
            
            db.session.add(user)
            db.session.commit()

    # Initialize default settings
    general_settings = GeneralSettings.query.first()
    if not general_settings:
        db.session.add(GeneralSettings())
        db.session.commit()

# ibject for all templates
@app.context_processor
def inject_settings():
    if current_user.is_anonymous:
        return dict(settings=None, card_settings=None)
    general_settings = GeneralSettings.query.first()
    card_settings = CardSettings.query.filter_by(user_id=current_user.id).first()
    settings = DashboardSettings.query.filter_by(user_id=current_user.id).first()  # Retrieve user-specific settings from DB
    feature_toggles_settings = FeatureTogglesSettings.query.filter_by(user_id=current_user.id).first()
    all_settings = dict(settings=settings, general_settings=general_settings, card_settings=card_settings, feature_toggles_settings=feature_toggles_settings)
    return all_settings
