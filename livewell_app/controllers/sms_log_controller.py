from flask import Blueprint, request, jsonify
from livewell_app import db
from livewell_app.models.sms_log import SMSLog
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

sms_log_bp = Blueprint('sms_log', __name__, url_prefix='/api/v1/sms-logs')

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

# Create a new SMS log entry (public access)
@sms_log_bp.route('/create', methods=['POST'])
def create_sms_log():
    try:
        data = request.get_json()
        new_sms_log = SMSLog(
            phone_number=data.get('phone_number'),
            message=data.get('message'),
            status=data.get('status'),
            sent_at=data.get('sent_at')
        )
        db.session.add(new_sms_log)
        db.session.commit()
        return jsonify({'message': 'SMS log created successfully', 'sms_log': {
            'id': new_sms_log.id,
            'phone_number': new_sms_log.phone_number,
            'message': new_sms_log.message,
            'status': new_sms_log.status,
            'sent_at': new_sms_log.sent_at.strftime('%Y-%m-%d %H:%M:%S')
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all SMS logs 
@sms_log_bp.route('/', methods=['GET'])
@admin_required
def get_all_sms_logs():
    logs = SMSLog.query.all()
    output = []
    for log in logs:
        log_data = {
            'id': log.id,
            'phone_number': log.phone_number,
            'message': log.message,
            'status': log.status,
            'sent_at': log.sent_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        output.append(log_data)
    return jsonify({'sms_logs': output})

# Get a specific SMS log entry 
@sms_log_bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_sms_log(id):
    log = SMSLog.query.get_or_404(id)
    log_data = {
        'id': log.id,
        'phone_number': log.phone_number,
        'message': log.message,
        'status': log.status,
        'sent_at': log.sent_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(log_data)

# Update an SMS log entry 
@sms_log_bp.route('/<int:id>', methods=['PUT'])
@admin_required  
def update_sms_log(id):
    log = SMSLog.query.get_or_404(id)
    data = request.get_json()

    try:
        log.phone_number = data.get('phone_number', log.phone_number)
        log.message = data.get('message', log.message)
        log.status = data.get('status', log.status)
        log.sent_at = data.get('sent_at', log.sent_at)

        db.session.commit()
        return jsonify({'message': 'SMS log updated successfully', 'sms_log': {
            'id': log.id,
            'phone_number': log.phone_number,
            'message': log.message,
            'status': log.status,
            'sent_at': log.sent_at.strftime('%Y-%m-%d %H:%M:%S')
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete an SMS log entry 
@sms_log_bp.route('/<int:id>', methods=['DELETE'])
@admin_required  
def delete_sms_log(id):
    try:
        log = SMSLog.query.get_or_404(id)
        db.session.delete(log)
        db.session.commit()
        return jsonify({'message': 'SMS log deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete SMS log', 'details': str(e)}), 500
