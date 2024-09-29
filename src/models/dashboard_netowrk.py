from src.config import db
from src.models.base_model import BaseModel


class DashboardNetworkSettings(BaseModel):
    """
    Dashboard network settings model for the application
    ---
    Properties:
        - id: int
        - name: the name of the dashboard
        - description: the description of the dashboard
        - ip_address: the IP address of the dashboard
        - port: the port of the dashboard
        - link: the link to the dashboard
    """
    __tablename__ = "DashboardGroup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    port = db.Column(db.Integer, nullable=True)
    link = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f"<DashboardGroup {self.name}, {self.description}>"
