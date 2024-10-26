from flask import Blueprint, request, jsonify
from livewell_app import db
from livewell_app.models.phone import Phone
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

phone_bp = Blueprint('phone', __name__, url_prefix='/api/v1/phones')

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

# Create a new phone entry (public access)
@phone_bp.route('/create', methods=['POST'])
def create_phone():
    try:
        data = request.get_json()
        new_phone = Phone(
            patient_name=data.get('patient_name'),
            phone_number=data.get('phone_number')
        )
        db.session.add(new_phone)
        db.session.commit()
        return jsonify({'message': 'Phone entry created successfully', 'phone': {
            'id': new_phone.id,
            'patient_name': new_phone.patient_name,
            'phone_number': new_phone.phone_number
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all phone entries 
@phone_bp.route('/', methods=['GET'])
@admin_required
def get_all_phones():
    phones = Phone.query.all()
    output = []
    for phone in phones:
        phone_data = {
            'id': phone.id,
            'patient_name': phone.patient_name,
            'phone_number': phone.phone_number
        }
        output.append(phone_data)
    return jsonify({'phones': output})

# Get a specific phone entry 
@phone_bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_phone(id):
    phone = Phone.query.get_or_404(id)
    phone_data = {
        'id': phone.id,
        'patient_name': phone.patient_name,
        'phone_number': phone.phone_number
    }
    return jsonify(phone_data)

# Update a phone entry 
@phone_bp.route('/<int:id>', methods=['PUT'])
@admin_required  
def update_phone(id):
    phone = Phone.query.get_or_404(id)
    data = request.get_json()

    try:
        phone.patient_name = data.get('patient_name', phone.patient_name)
        phone.phone_number = data.get('phone_number', phone.phone_number)

        db.session.commit()
        return jsonify({'message': 'Phone entry updated successfully', 'phone': {
            'id': phone.id,
            'patient_name': phone.patient_name,
            'phone_number': phone.phone_number
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a phone entry 
@phone_bp.route('/<int:id>', methods=['DELETE'])
@admin_required  
def delete_phone(id):
    try:
        phone = Phone.query.get_or_404(id)
        db.session.delete(phone)
        db.session.commit()
        return jsonify({'message': 'Phone entry deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete phone entry', 'details': str(e)}), 500
