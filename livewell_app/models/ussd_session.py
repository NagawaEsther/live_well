from livewell_app import db
from datetime import datetime

class USSDSession(db.Model):
    __tablename__ = 'ussd_sessions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, unique=True)  # Unique identifier for the session
    phone_number = db.Column(db.String(20), nullable=False)  # Phone number of the user
    session_data = db.Column(db.Text, nullable=True)  # Data stored during the session (e.g., user inputs)
    status = db.Column(db.String(20), nullable=False, default='active')  # Status of the session (e.g., active, completed)
    service_code = db.Column(db.String(20), nullable=True)  # Optional: Service code for the USSD session
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp for session creation
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Timestamp for session updates
    terminated_at = db.Column(db.DateTime, nullable=True)  # Optional timestamp for when the session was terminated

    def __init__(self, session_id, phone_number, session_data=None, status='active', service_code=None):
        self.session_id = session_id
        self.phone_number = phone_number
        self.session_data = session_data
        self.status = status
        self.service_code = service_code

    def __repr__(self):
        return (f"<USSDSession(session_id='{self.session_id}', phone_number='{self.phone_number}', "
                f"status='{self.status}', service_code='{self.service_code}', "
                f"created_at='{self.created_at}')>")
