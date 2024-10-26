from datetime import datetime
from livewell_app.extensions import db

class SMSLog(db.Model):
    __tablename__ = 'sms_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, phone_number, message, status, sent_at=None):
        self.phone_number = phone_number
        self.message = message
        self.status = status
        self.sent_at = sent_at if sent_at else datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'message': self.message,
            'status': self.status,
            'sent_at': self.sent_at.strftime('%Y-%m-%d %H:%M:%S')
        }
