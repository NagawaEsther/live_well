from flask import Blueprint, request, jsonify
from livewell_app import db
from livewell_app.models.medical_record import MedicalRecord
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

medical_record_bp = Blueprint('medical_record', __name__, url_prefix='/api/v1/medical-records')

# Admin required
def admin_required(fn):
    @wraps(fn)
    @jwt_required()  
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Create a new medical record (public access)
@medical_record_bp.route('/create', methods=['POST'])
def create_medical_record():
    try:
        data = request.get_json()
        new_record = MedicalRecord(
            patient_name=data.get('patient_name'),
            doctor_name=data.get('doctor_name'),
            diagnosis=data.get('diagnosis'),
            treatment=data.get('treatment'),
            record_date=data.get('record_date')
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Medical record created successfully', 'record': {
            'id': new_record.id,
            'patient_name': new_record.patient_name,
            'doctor_name': new_record.doctor_name,
            'diagnosis': new_record.diagnosis,
            'treatment': new_record.treatment,
            'record_date': new_record.record_date.strftime('%Y-%m-%d %H:%M:%S')
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all medical records 
@medical_record_bp.route('/', methods=['GET'])
@admin_required
def get_all_medical_records():
    records = MedicalRecord.query.all()
    output = []
    for record in records:
        record_data = {
            'id': record.id,
            'patient_name': record.patient_name,
            'doctor_name': record.doctor_name,
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'record_date': record.record_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        output.append(record_data)
    return jsonify({'records': output})

# Get a specific medical record 
@medical_record_bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_medical_record(id):
    record = MedicalRecord.query.get_or_404(id)
    record_data = {
        'id': record.id,
        'patient_name': record.patient_name,
        'doctor_name': record.doctor_name,
        'diagnosis': record.diagnosis,
        'treatment': record.treatment,
        'record_date': record.record_date.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(record_data)

# Update a medical record 
@medical_record_bp.route('/<int:id>', methods=['PUT'])
@admin_required  
def update_medical_record(id):
    record = MedicalRecord.query.get_or_404(id)
    data = request.get_json()

    try:
        record.patient_name = data.get('patient_name', record.patient_name)
        record.doctor_name = data.get('doctor_name', record.doctor_name)
        record.diagnosis = data.get('diagnosis', record.diagnosis)
        record.treatment = data.get('treatment', record.treatment)
        record.record_date = data.get('record_date', record.record_date)

        db.session.commit()
        return jsonify({'message': 'Medical record updated successfully', 'record': {
            'id': record.id,
            'patient_name': record.patient_name,
            'doctor_name': record.doctor_name,
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'record_date': record.record_date.strftime('%Y-%m-%d %H:%M:%S')
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a medical record 
@medical_record_bp.route('/<int:id>', methods=['DELETE'])
@admin_required  
def delete_medical_record(id):
    try:
        record = MedicalRecord.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'Medical record deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete medical record', 'details': str(e)}), 500
