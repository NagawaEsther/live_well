from flask import Blueprint, request, jsonify
from livewell_app import db
from livewell_app.models.voice_call_log import VoiceCall
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime



voice_call_log_bp = Blueprint('voice_call_log', __name__, url_prefix='/api/v1/voice-call-log')


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


# Create a new voice call log (Admin access only)
@voice_call_log_bp.route('/create', methods=['POST'])
@admin_required
def create_voice_call_log():
    data = request.get_json()
    try:
        new_call_log = VoiceCall(
            call_id=data.get('call_id'),  # Changed from caller_id to call_id
            caller_number=data.get('caller_number'),  # Changed from recipient_id to caller_number
            receiver_number=data.get('receiver_number'),  # Changed from recipient_id to receiver_number
            call_status=data.get('call_status', 'initiated'),  # Default status set to 'initiated'
            duration=data.get('duration'),  # Optional field
            recording_url=data.get('recording_url'),  # Optional field
            failure_reason=data.get('failure_reason')  # Optional field
        )
        db.session.add(new_call_log)
        db.session.commit()
        return jsonify({
            'message': 'Voice call log created successfully',
            'call_log': {
                'id': new_call_log.id,
                'call_id': new_call_log.call_id,
                'caller_number': new_call_log.caller_number,
                'receiver_number': new_call_log.receiver_number,
                'call_status': new_call_log.call_status,
                'duration': new_call_log.duration,
                'recording_url': new_call_log.recording_url,
                'failure_reason': new_call_log.failure_reason,
                'initiated_at': new_call_log.initiated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'terminated_at': new_call_log.terminated_at.strftime('%Y-%m-%d %H:%M:%S') if new_call_log.terminated_at else None
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get all voice call logs (Admin access only)
@voice_call_log_bp.route('/all', methods=['GET'])
@admin_required
def get_all_voice_call_logs():
    logs = VoiceCall.query.all()
    output = []
    for log in logs:
        log_data = {
            'id': log.id,
            'call_id': log.call_id,
            'caller_number': log.caller_number,
            'receiver_number': log.receiver_number,
            'call_status': log.call_status,
            'duration': log.duration,
            'recording_url': log.recording_url,
            'failure_reason': log.failure_reason,
            'initiated_at': log.initiated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'terminated_at': log.terminated_at.strftime('%Y-%m-%d %H:%M:%S') if log.terminated_at else None
        }
        output.append(log_data)
    return jsonify({'voice_call_logs': output})


# Get a specific voice call log by ID (Admin access only)
@voice_call_log_bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_voice_call_log(id):
    log = VoiceCall.query.get_or_404(id)
    log_data = {
        'id': log.id,
        'call_id': log.call_id,
        'caller_number': log.caller_number,
        'receiver_number': log.receiver_number,
        'call_status': log.call_status,
        'duration': log.duration,
        'recording_url': log.recording_url,
        'failure_reason': log.failure_reason,
        'initiated_at': log.initiated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'terminated_at': log.terminated_at.strftime('%Y-%m-%d %H:%M:%S') if log.terminated_at else None
    }
    return jsonify(log_data)


# Update a voice call log (Admin access only)
@voice_call_log_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_voice_call_log(id):
    log = VoiceCall.query.get_or_404(id)
    data = request.get_json()

    try:
        log.call_id = data.get('call_id', log.call_id)
        log.caller_number = data.get('caller_number', log.caller_number)
        log.receiver_number = data.get('receiver_number', log.receiver_number)
        log.call_status = data.get('call_status', log.call_status)
        log.duration = data.get('duration', log.duration)
        log.recording_url = data.get('recording_url', log.recording_url)
        log.failure_reason = data.get('failure_reason', log.failure_reason)
        log.terminated_at = datetime.utcnow() if data.get('terminated') else log.terminated_at  # Set terminated_at if needed
        
        db.session.commit()
        return jsonify({
            'message': 'Voice call log updated successfully',
            'call_log': {
                'id': log.id,
                'call_id': log.call_id,
                'caller_number': log.caller_number,
                'receiver_number': log.receiver_number,
                'call_status': log.call_status,
                'duration': log.duration,
                'recording_url': log.recording_url,
                'failure_reason': log.failure_reason,
                'initiated_at': log.initiated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'terminated_at': log.terminated_at.strftime('%Y-%m-%d %H:%M:%S') if log.terminated_at else None
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Delete a voice call log (Admin access only)
@voice_call_log_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_voice_call_log(id):
    log = VoiceCall.query.get_or_404(id)
    try:
        db.session.delete(log)
        db.session.commit()
        return jsonify({'message': 'Voice call log deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete voice call log', 'details': str(e)}), 500
