from src.models.base_model import BaseModel
from src.config import db

class NotificationSettings(BaseModel):
    """
    Notification settings for Slack, Discord, and Teams.
    """

    id = db.Column(db.Integer, primary_key=True)
    slack_webhook_url = db.Column(db.String(150), nullable=False)
    discord_webhook_url = db.Column(db.String(150), nullable=False)
    teams_webhook_url = db.Column(db.String(150), nullable=False)
    google_chat_webhook_url = db.Column(db.String(150), nullable=False)
    telegram_webhook_url = db.Column(db.String(150), nullable=False)
    telegram_chat_id = db.Column(db.String(150), nullable=False)

    is_email_alert_enabled = db.Column(db.Boolean, default=False)
    is_slack_alert_enabled = db.Column(db.Boolean, default=False)
    is_discord_alert_enabled = db.Column(db.Boolean, default=False)
    is_teams_alert_enabled = db.Column(db.Boolean, default=False)
    is_google_chat_alert_enabled = db.Column(db.Boolean, default=False)
    is_telegram_alert_enabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<NotificationSettings>"

    @staticmethod
    def to_dict():
        notification_settings = NotificationSettings.query.first()
        return {
            "slack_webhook_url": notification_settings.slack_webhook_url,
            "discord_webhook_url": notification_settings.discord_webhook_url,
            "teams_webhook_url": notification_settings.teams_webhook_url,
            "google_chat_webhook_url": notification_settings.google_chat_webhook_url,
            "telegram_webhook_url": notification_settings.telegram_webhook_url,
            "telegram_chat_id": notification_settings.telegram_chat_id,
            "is_email_alert_enabled": notification_settings.is_email_alert_enabled,
            "is_slack_alert_enabled": notification_settings.is_slack_alert_enabled,
            "is_discord_alert_enabled": notification_settings.is_discord_alert_enabled,
            "is_teams_alert_enabled": notification_settings.is_teams_alert_enabled,
            "is_google_chat_alert_enabled": notification_settings.is_google_chat_alert_enabled,
            "is_telegram_alert_enabled": notification_settings.is_telegram_alert_enabled
        }

    @staticmethod
    def get_slack_webhook_url():
        return NotificationSettings.query.first().slack_webhook_url

    @staticmethod
    def get_discord_webhook_url():
        return NotificationSettings.query.first().discord_webhook_url

    @staticmethod
    def get_teams_webhook_url():
        return NotificationSettings.query.first().teams_webhook_url
    
    @staticmethod
    def get_google_chat_webhook_url():
        return NotificationSettings.query.first().google_chat_webhook_url
    
    @staticmethod
    def get_telegram_webhook_url():
        return NotificationSettings.query.first().telegram_webhook_url
    
    @staticmethod
    def get_telegram_chat_id():
        return NotificationSettings.query.first().telegram_chat_id
