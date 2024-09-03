from src.config import db

class ApplicationGeneralSettings(db.Model):
    __tablename__ = 'general_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    enable_alerts = db.Column(db.Boolean, default=True)
    timezone = db.Column(db.String(50), default='UTC')
    enable_cache = db.Column(db.Boolean, default=True)
    
