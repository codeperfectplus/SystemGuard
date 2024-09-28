from src.config import db

class NotificationSettings(db.Model):
    """
    slack_webhook_url: the webhook URL for the Slack channel
    discord_webhook_url: the webhook URL for the Discord channel
    teams_webhook_url: the webhook URL for the Microsoft Teams channel
    """

    id = db.Column(db.Integer, primary_key=True)
    slack_webhook_url = db.Column(db.String(150), nullable=False)
    discord_webhook_url = db.Column(db.String(150), nullable=False)
    teams_webhook_url = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<NotificationSettings (Slack: {self.slack_webhook_url})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "slack_webhook_url": self.slack_webhook_url,
            "discord_webhook_url": self.discord_webhook_url,
            "teams_webhook_url": self.teams_webhook_url
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return NotificationSettings.query.all()
    
    @staticmethod
    def get_by_id(notification_id):
        return NotificationSettings.query.get(notification_id)
    
    # get slack webhook url
    @staticmethod
    def get_slack_webhook_url():
        return NotificationSettings.query.first().slack_webhook_url


    @staticmethod
    def get_discord_webhook_url():
        return NotificationSettings.query.first().discord_webhook_url
    
    @staticmethod
    def get_teams_webhook_url():
        return NotificationSettings.query.first().teams_webhook_url