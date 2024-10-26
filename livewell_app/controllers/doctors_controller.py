from flask import Blueprint, request, jsonify
from livewell_app import db
from livewell_app.models.doctors import Doctor
from flask_jwt_extended import jwt_required

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/api/v1/doctors')

# Get all doctors (open access)
@doctor_bp.route('/doctors', methods=['GET'])
def get_all_doctors():
    try:
        doctors = Doctor.query.all()
        output = []

        for doctor in doctors:
            doctor_data = {
                'id': doctor.id,
                'name': doctor.name,
                'email': doctor.email,
                'contact_number': doctor.contact_number,
                'specialty': doctor.specialty,
                'bio_data': doctor.bio_data
            }
            output.append(doctor_data)

        return jsonify({'doctors': output}), 200

    except Exception as e:
        print("Error fetching doctors:", str(e))
        return jsonify({'error': 'An error occurred while fetching doctors', 'details': str(e)}), 500

# Get a single doctor by ID (open access)
@doctor_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        doctor_data = {
            'id': doctor.id,
            'name': doctor.name,
            'email': doctor.email,
            'contact_number': doctor.contact_number,
            'specialty': doctor.specialty,
            'bio_data': doctor.bio_data
        }
        return jsonify(doctor_data), 200

    except Exception as e:
        print("Error fetching doctor:", str(e))
        return jsonify({'error': 'An error occurred while fetching the doctor', 'details': str(e)}), 500

# Create a new doctor (open access)
@doctor_bp.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400

    try:
        new_doctor = Doctor(
            name=data.get('name'),
            email=data.get('email'),
            contact_number=data.get('contact_number'),
            specialty=data.get('specialty'),
            bio_data=data.get('bio_data', True)  # Default to True if not provided
        )
        db.session.add(new_doctor)
        db.session.commit()

        return jsonify({
            'message': 'Doctor created successfully',
            'doctor': {
                'id': new_doctor.id,
                'name': new_doctor.name,
                'email': new_doctor.email,
                'contact_number': new_doctor.contact_number,
                'specialty': new_doctor.specialty,
                'bio_data': new_doctor.bio_data
            }
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        print("Error creating doctor:", str(e))
        return jsonify({'error': 'An error occurred while creating the doctor', 'details': str(e)}), 500

# Update a doctor's details (open access)
@doctor_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.get_json()

    if data.get('name'):
        doctor.name = data['name']
    if data.get('email'):
        doctor.email = data['email']
    if data.get('contact_number'):
        doctor.contact_number = data['contact_number']
    if data.get('specialty'):
        doctor.specialty = data['specialty']
    if data.get('bio_data') is not None:  # Allow False to be set
        doctor.bio_data = data['bio_data']

    try:
        db.session.commit()
        return jsonify({'message': 'Doctor updated successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        print("Error updating doctor:", str(e))
        return jsonify({'error': 'An error occurred while updating the doctor', 'details': str(e)}), 500

# Delete a doctor (open access)
@doctor_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)

    try:
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({'message': 'Doctor deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        print("Error deleting doctor:", str(e))
        return jsonify({'error': 'An error occurred while deleting the doctor', 'details': str(e)}), 500
