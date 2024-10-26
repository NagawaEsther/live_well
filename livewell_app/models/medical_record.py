from livewell_app import db
from datetime import datetime

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # References a patient in the User table
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # References a doctor in the User table
    diagnosis = db.Column(db.String(255), nullable=False)  # Diagnosis details
    treatment = db.Column(db.Text, nullable=True)  # Description of the treatment prescribed
    notes = db.Column(db.Text, nullable=True)  # Additional notes or observations
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Date of the record creation
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Timestamp for updates

    def __init__(self, patient_id, doctor_id, diagnosis, treatment=None, notes=None):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.notes = notes

    def __repr__(self):
        return f"<MedicalRecord {self.id} for Patient {self.patient_id} by Doctor {self.doctor_id}>"
