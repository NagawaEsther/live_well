from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from livewell_app.extensions import db, Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # Automatically set to 'doctor' or 'patient'
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    is_doctor = db.Column(db.Boolean, default=False)  # True for doctors, False for patients
    specialty = db.Column(db.String(100), nullable=True)  # Specialty of the doctor
    medical_history = db.Column(db.Text, nullable=True)  # Patient's medical history
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, name, email, password, date_of_birth, contact_number, address, is_doctor=False, specialty=None, medical_history=None):
        self.name = name
        self.email = email
        self.password_hash = password  # Store plain password temporarily for hashing
        self.role = 'doctor' if is_doctor else 'patient'  # Automatically set role based on is_doctor
        self.date_of_birth = date_of_birth
        self.contact_number = contact_number
        self.address = address
        self.is_doctor = is_doctor
        self.specialty = specialty if is_doctor else None
        self.medical_history = medical_history if not is_doctor else None

    def hash_password(self):
        self.password_hash = bcrypt.generate_password_hash(self.password_hash).decode('utf-8')
        # self.password_hash = None  

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def signup(cls, name, email, password, date_of_birth, contact_number, address, is_doctor=False, specialty=None, medical_history=None):
        if cls.query.filter_by(email=email).first():
            raise ValueError("Email already exists")
        
        user = cls(
            name=name,
            email=email,
            password=password,  
            date_of_birth=date_of_birth,
            contact_number=contact_number,
            address=address,
            is_doctor=is_doctor,
            specialty=specialty,
            medical_history=medical_history
        )
        
        user.hash_password()  # Hash the password before committing to the database

        db.session.add(user)
        db.session.commit()

    @classmethod
    def login(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        raise ValueError("Invalid email or password")

    def __repr__(self):
        return f"<User {self.name} ({'Doctor' if self.is_doctor else 'Patient'})>"
    
    
   