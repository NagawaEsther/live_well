from livewell_app import db
from datetime import datetime

class Phone(db.Model):
    __tablename__ = 'phones'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # References the user who owns this phone number
    phone_number = db.Column(db.String(20), nullable=False, unique=True)  # Phone number
    type = db.Column(db.String(20), nullable=False, default="mobile")  # Type of phone, e.g., mobile, landline
    is_primary = db.Column(db.Boolean, nullable=False, default=False)  # Indicates if this is the primary contact number
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp for record creation
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Timestamp for updates

    def __init__(self, user_id, phone_number, type="mobile", is_primary=False):
        self.user_id = user_id
        self.phone_number = phone_number
        self.type = type
        self.is_primary = is_primary

    def __repr__(self):
        return f"<Phone {self.phone_number} (Type: {self.type}) - Primary: {self.is_primary}>"
