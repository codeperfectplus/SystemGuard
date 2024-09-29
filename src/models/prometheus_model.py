from src.config import db
from src.models.base_model import BaseModel


class ExternalMonitornig(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
