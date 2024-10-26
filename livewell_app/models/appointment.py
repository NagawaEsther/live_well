from livewell_app import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(125),nullable=False)  
    doctor_name = db.Column(db.String(125), nullable=False)  # Stores doctor's name instead of ID
    appointment_time = db.Column(db.DateTime, nullable=False)  # Scheduled time for the appointment
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Date when the appointment was made
    status = db.Column(db.String(20), nullable=False, default='scheduled')  # Appointment status
    notes = db.Column(db.Text, nullable=True)  # Optional notes for the appointment

    def __init__(self, patient_name, doctor_name, appointment_time, status='scheduled', notes=None):
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.appointment_time = appointment_time
        self.status = status
        self.notes = notes

    def __repr__(self):
        return f"<Appointment {self.id} between Patient {self.patient_id} and Doctor {self.doctor_name} - Status: {self.status}>"
