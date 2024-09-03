from src.config import db, app


class DashboardCard(db.Model):
    __tablename__ = 'dashboard_cards'
    
    id = db.Column(db.Integer, primary_key=True)                  # Primary key field
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))    # Foreign key to the user
    card_name = db.Column(db.String(100), nullable=False)         # Name of the card
    card_description = db.Column(db.Text, nullable=True)          # Description of the card
    card_data = db.Column(db.JSON, nullable=True)                 # Data associated with the card (could be JSON)
    card_icon = db.Column(db.String(100), nullable=True)          # Icon associated with the card
    card_color = db.Column(db.String(7), default='#ffffff')       # Color of the card in hex format
    card_length = db.Column(db.Integer, default="small")          # small, medium, large
    card_position = db.Column(db.Integer, default=0)              # Position of the card on the dashboard
    card_enabled = db.Column(db.Boolean, default=True)            # Is the card enabled on the dashboard
    
    def __repr__(self):
        return f'<DashboardCard {self.card_name}>'

