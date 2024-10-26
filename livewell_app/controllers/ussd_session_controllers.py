from flask import Blueprint, request, jsonify
from livewell_app import db
from livewell_app.models.ussd_session import USSDSession
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

ussd_session_bp = Blueprint('ussd_session', __name__, url_prefix='/api/v1/ussd-sessions')

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

# Create a new USSD session entry (public access)
@ussd_session_bp.route('/create', methods=['POST'])
def create_ussd_session():
    try:
        data = request.get_json()
        new_ussd_session = USSDSession(
            session_id=data.get('session_id'),  # Assuming session_id is provided in the request
            phone_number=data.get('phone_number'),
            session_data=data.get('session_data'),
            status=data.get('status', 'active')  # Default to 'active' if not provided
        )
        db.session.add(new_ussd_session)
        db.session.commit()
        return jsonify({
            'message': 'USSD session created successfully',
            'ussd_session': {
                'id': new_ussd_session.id,
                'session_id': new_ussd_session.session_id,
                'phone_number': new_ussd_session.phone_number,
                'session_data': new_ussd_session.session_data,
                'status': new_ussd_session.status,
                'created_at': new_ussd_session.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all USSD sessions (admin only)
@ussd_session_bp.route('/', methods=['GET'])
@admin_required
def get_all_ussd_sessions():
    sessions = USSDSession.query.all()
    output = []
    for session in sessions:
        session_data = {
            'id': session.id,
            'session_id': session.session_id,
            'phone_number': session.phone_number,
            'session_data': session.session_data,
            'status': session.status,
            'created_at': session.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        output.append(session_data)
    return jsonify({'ussd_sessions': output})

# Get a specific USSD session entry (admin only)
@ussd_session_bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_ussd_session(id):
    session = USSDSession.query.get_or_404(id)
    session_data = {
        'id': session.id,
        'session_id': session.session_id,
        'phone_number': session.phone_number,
        'session_data': session.session_data,
        'status': session.status,
        'created_at': session.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(session_data)

# Update a USSD session entry (admin only)
@ussd_session_bp.route('/<int:id>', methods=['PUT'])
@admin_required  
def update_ussd_session(id):
    session = USSDSession.query.get_or_404(id)
    data = request.get_json()

    try:
        session.phone_number = data.get('phone_number', session.phone_number)
        session.session_data = data.get('session_data', session.session_data)
        session.status = data.get('status', session.status)  # Updated the attribute name to match the model

        db.session.commit()
        return jsonify({
            'message': 'USSD session updated successfully',
            'ussd_session': {
                'id': session.id,
                'session_id': session.session_id,
                'phone_number': session.phone_number,
                'session_data': session.session_data,
                'status': session.status,
                'created_at': session.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a USSD session entry (admin only)
@ussd_session_bp.route('/<int:id>', methods=['DELETE'])
@admin_required  
def delete_ussd_session(id):
    try:
        session = USSDSession.query.get_or_404(id)
        db.session.delete(session)
        db.session.commit()
        return jsonify({'message': 'USSD session deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete USSD session', 'details': str(e)}), 500
