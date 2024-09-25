from src.config import db

class GeneralSettings(db.Model):
    """
    General settings model for the application
    ---
    Properties:
        - id: int
        - enable_alerts: if email alerts are enabled
        - timezone: the timezone of the system
        - enable_cache: if caching is enabled
        - is_logging_system_info: if system info is logged
    """
    __tablename__ = 'general_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    enable_alerts = db.Column(db.Boolean, default=True)
    timezone = db.Column(db.String(50), default='UTC')
    enable_cache = db.Column(db.Boolean, default=True)
    is_logging_system_info = db.Column(db.Boolean, default=True)    
