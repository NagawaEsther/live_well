from livewell_app import db
from datetime import datetime

class VoiceCall(db.Model):
    __tablename__ = 'voice_calls'
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.String(100), nullable=False, unique=True)  # Unique identifier for the call
    caller_number = db.Column(db.String(20), nullable=False)  # Phone number of the caller
    receiver_number = db.Column(db.String(20), nullable=False)  # Phone number of the receiver
    call_status = db.Column(db.String(20), nullable=False, default='initiated')  # Status of the call (e.g., initiated, in progress, completed, failed)
    duration = db.Column(db.Integer, nullable=True)  # Duration of the call in seconds
    recording_url = db.Column(db.String(255), nullable=True)  # URL of the recording, if applicable
    failure_reason = db.Column(db.String(255), nullable=True)  # Reason for failure, if any
    initiated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp for call initiation
    terminated_at = db.Column(db.DateTime, nullable=True)  # Optional timestamp for when the call was terminated

    def __init__(self, call_id, caller_number, receiver_number, call_status='initiated', duration=None, recording_url=None, failure_reason=None):
        self.call_id = call_id
        self.caller_number = caller_number
        self.receiver_number = receiver_number
        self.call_status = call_status
        self.duration = duration
        self.recording_url = recording_url
        self.failure_reason = failure_reason

    def __repr__(self):
        return (f"<VoiceCall(call_id='{self.call_id}', caller='{self.caller_number}', "
                f"receiver='{self.receiver_number}', status='{self.call_status}', "
                f"initiated_at='{self.initiated_at}', duration='{self.duration}', "
                f"recording_url='{self.recording_url}', failure_reason='{self.failure_reason}')>")
