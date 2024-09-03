from src.config import db


class DashboardNetworkSettings(db.Model):
    __tablename__ = "DashboardGroup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    port = db.Column(db.Integer, nullable=True)
    link = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f"<DashboardGroup {self.name}, {self.description}>"
