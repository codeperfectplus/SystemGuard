from src.config import db


class UserCardSettings(db.Model):
    """
    User card settings model for the application
    ---
    Properties:
        - id: int
        - user_id: the user id
        - is_user_card_enabled: if the user card is enabled
        - is_server_card_enabled: if the server card is enabled
        - is_battery_card_enabled: if the battery card is enabled
        - is_cpu_core_card_enabled: if the CPU core card is enabled
        - is_cpu_usage_card_enabled: if the CPU usage card is enabled
        - is_cpu_temp_card_enabled: if the CPU temp card is enabled
        - is_dashboard_memory_card_enabled: if the dashboard memory card is enabled
        - is_memory_usage_card_enabled: if the memory usage card is enabled
        - is_disk_usage_card_enabled: if the disk usage card is enabled
        - is_system_uptime_card_enabled: if the system uptime card is enabled
        - is_network_statistic_card_enabled: if the network statistic card is enabled
        - is_speedtest_enabled: if speedtests are enabled
    """
    __tablename__ = "user_card_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

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
