from sqlalchemy import Column, Integer, String, Boolean
from livewell_app import db  
class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    contact_number = Column(String(15), nullable=False)
    specialty = Column(String(100))
    bio_data = Column(String(500), nullable=False)

    def __repr__(self):
        return f"<Doctor {self.name}>"
