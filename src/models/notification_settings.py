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


    def __repr__(self):
        return f"<NotificationSettings (Slack: {self.slack_webhook_url})>"

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
