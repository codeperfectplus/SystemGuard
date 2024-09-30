from src.models.base_model import BaseModel
from src.config import db


# alert Data model to save the prometheus alert data
class AlertDataModel(BaseModel):
    __tablename__ = "alert_data"

    id = db.Column(db.Integer, primary_key=True)
    alert_name = db.Column(db.String(255), nullable=False)
    instance = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<AlertData {self.alert_name}>"
    
    def serialize(self):
        return {
            'id': self.id,
            'alert_name': self.alert_name,
            'instance': self.instance,
            'severity': self.severity,
            'description': self.description,
            'summary': self.summary,
            'status': self.status,
            'start_time': self.start_time
        }
