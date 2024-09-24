from src.config import db

class PageToggleSettings(db.Model):
    """
    Page toggle settings model for the application
    ---
    Properties:
        - id: int
        - user_id: the user id
        - is_cpu_info_enabled: if CPU info is enabled
        - is_memory_info_enabled: if memory info is enabled
        - is_disk_info_enabled: if disk info is enabled
        - is_network_info_enabled: if network info is enabled
        - is_process_info_enabled: if process info is enabled
        - is_dashboard_network_enabled: if the dashboard network is enabled
    """
    __tablename__ = 'feature_toggle_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Feature Toggles
    is_cpu_info_enabled = db.Column(db.Boolean, default=True)
    is_memory_info_enabled = db.Column(db.Boolean, default=True)
    is_disk_info_enabled = db.Column(db.Boolean, default=True)
    is_network_info_enabled = db.Column(db.Boolean, default=True)
    is_process_info_enabled = db.Column(db.Boolean, default=True)
    is_dashboard_network_enabled = db.Column(db.Boolean, default=True)
