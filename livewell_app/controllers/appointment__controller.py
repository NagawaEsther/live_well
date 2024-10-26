from flask import Blueprint, request, jsonify
from livewell_app import db
from livewell_app.models.appointment import Appointment
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

appointment_bp = Blueprint('appointment', __name__, url_prefix='/api/v1/appointments')

# Admin required decorator
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Create a new appointment
@appointment_bp.route('/create', methods=['POST'])
def create_appointment():
    try:
        data = request.get_json()
        new_appointment = Appointment(
            patient_name=data.get('patient_name'),  # Use patient_name instead of patient_id
            doctor_name=data.get('doctor_name'),
            appointment_time=data.get('appointment_time'),
            status=data.get('status', 'scheduled'),
            notes=data.get('notes')
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment created successfully', 'appointment': {
            'id': new_appointment.id,
            'patient_name': new_appointment.patient_name,
            'doctor_name': new_appointment.doctor_name,
            'appointment_time': new_appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': new_appointment.status,
            'notes': new_appointment.notes
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all appointments
@appointment_bp.route('/', methods=['GET'])
@admin_required
def get_all_appointments():
    appointments = Appointment.query.all()
    output = []
    for appointment in appointments:
        appointment_data = {
            'id': appointment.id,
            'patient_name': appointment.patient_name,
            'doctor_name': appointment.doctor_name,
            'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': appointment.status,
            'notes': appointment.notes
        }
        output.append(appointment_data)
    return jsonify({'appointments': output})

# Get a specific appointment
@appointment_bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment_data = {
        'id': appointment.id,
        'patient_name': appointment.patient_name,
        'doctor_name': appointment.doctor_name,
        'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
        'status': appointment.status,
        'notes': appointment.notes
    }
    return jsonify(appointment_data)

# Update an appointment
@appointment_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    data = request.get_json()

    try:
        appointment.patient_name = data.get('patient_name', appointment.patient_name)  # Update patient_name
        appointment.doctor_name = data.get('doctor_name', appointment.doctor_name)
        appointment.appointment_time = data.get('appointment_time', appointment.appointment_time)
        appointment.status = data.get('status', appointment.status)
        appointment.notes = data.get('notes', appointment.notes)

        db.session.commit()
        return jsonify({'message': 'Appointment updated successfully', 'appointment': {
            'id': appointment.id,
            'patient_name': appointment.patient_name,
            'doctor_name': appointment.doctor_name,
            'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': appointment.status,
            'notes': appointment.notes
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete an appointment
@appointment_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_appointment(id):
    try:
        appointment = Appointment.query.get_or_404(id)
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete appointment', 'details': str(e)}), 500
