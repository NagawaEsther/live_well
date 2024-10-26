# from flask import Blueprint, request, jsonify
# from livewell_app import db, bcrypt
# from livewell_app.models.user import User
# from functools import wraps
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# user_bp = Blueprint('user', _name_, url_prefix='/api/v1/users')

# # Admin required
# def admin_required(fn):
#     @wraps(fn)
#     @jwt_required()
#     def wrapper(*args, **kwargs):
#         user_info = get_jwt_identity()
#         if user_info['role'] != 'admin':
#             return jsonify({'error': 'Admin access required'}), 403
#         return fn(*args, **kwargs)
#     return wrapper

# # User Registration (Public access)
# @user_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     if not data or not data.get('email') or not data.get('password'):
#         return jsonify({'error': 'Email and password are required'}), 400
    
#     if User.query.filter_by(email=data.get('email')).first():
#         return jsonify({'error': 'Email already registered'}), 400

#     # Hash the password
#     hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    
#     # Create new user instance
#     new_user = User(
#         name=data.get('name'),
#         email=data.get('email'),
#         password=hashed_password,
#         role=data.get('role', 'patient'),  # Default role as 'patient'
#         date_of_birth=data.get('date_of_birth'),
#         contact_number=data.get('contact_number'),
#         address=data.get('address'),
#         is_doctor=data.get('is_doctor', False),
#         specialty=data.get('specialty'),
#         medical_history=data.get('medical_history')
#     )
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully', 'user': {'id': new_user.id, 'name': new_user.name, 'email': new_user.email, 'role': new_user.role}}), 201

# # User Login (Public access)
# @user_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not data.get('email') or not data.get('password'):
#         return jsonify({'error': 'Email and password are required'}), 400

#     user = User.query.filter_by(email=data.get('email')).first()

#     if user and user.check_password(data.get('password')):  # Using check_password method
#         access_token = create_access_token(identity={'id': user.id, 'role': user.role})
#         return jsonify({'token': access_token, 'user': {
#             'id': user.id,
#             'name': user.name,
#             'email': user.email,
#             'role': user.role
#         }}), 200
    
#     return jsonify({'error': 'Invalid email or password'}), 401

# # Get All Users (Admin only)
# @user_bp.route('/', methods=['GET'])
# @admin_required
# def get_all_users():
#     users = User.query.all()
#     output = []
#     for user in users:
#         user_data = {
#             'id': user.id,
#             'name': user.name,
#             'email': user.email,
#             'role': user.role,
#             'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
#         }
#         output.append(user_data)
#     return jsonify({'users': output})

# # Get Single User (Admin or user’s own access)
# @user_bp.route('/<int:id>', methods=['GET'])
# @jwt_required()
# def get_user(id):
#     current_user = get_jwt_identity()
#     user = User.query.get_or_404(id)

#     if current_user['role'] != 'admin' and current_user['id'] != user.id:
#         return jsonify({'error': 'Unauthorized access'}), 403

#     user_data = {
#         'id': user.id,
#         'name': user.name,
#         'email': user.email,
#         'role': user.role,
#         'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
#         'contact_number': user.contact_number,
#         'address': user.address,
#         'is_doctor': user.is_doctor,
#         'specialty': user.specialty,
#         'medical_history': user.medical_history,
#         'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
#     }
#     return jsonify(user_data)

# # Update User (Admin or user’s own access)
# @user_bp.route('/<int:id>', methods=['PUT'])
# @jwt_required()
# def update_user(id):
#     current_user = get_jwt_identity()
#     user = User.query.get_or_404(id)

#     if current_user['role'] != 'admin' and current_user['id'] != user.id:
#         return jsonify({'error': 'Unauthorized access'}), 403

#     data = request.get_json()

#     user.name = data.get('name', user.name)
#     user.email = data.get('email', user.email)
#     if data.get('password'):
#         user.password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
#     user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
#     user.contact_number = data.get('contact_number', user.contact_number)
#     user.address = data.get('address', user.address)
#     user.is_doctor = data.get('is_doctor', user.is_doctor)
#     user.specialty = data.get('specialty', user.specialty)
#     user.medical_history = data.get('medical_history', user.medical_history)

#     db.session.commit()

#     return jsonify({'message': 'User updated successfully', 'user': {
#         'id': user.id,
#         'name': user.name,
#         'email': user.email,
#         'role': user.role
#     }})

# # Delete User (Admin only)
# @user_bp.route('/<int:id>', methods=['DELETE'])
# @admin_required
# def delete_user(id):
#     user = User.query.get_or_404(id)
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'User deleted successfully'}), 200


from flask import Blueprint, request, jsonify
from livewell_app import db,bcrypt
from livewell_app.models.user import User
from functools import wraps
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')

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

# User Registration (Public access)
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    try:
        User.signup(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),
            date_of_birth=data.get('date_of_birth'),
            contact_number=data.get('contact_number'),
            address=data.get('address'),
            is_doctor=data.get('is_doctor', False),
            specialty=data.get('specialty'),
            medical_history=data.get('medical_history')
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'User registered successfully', }), 201

# User Login (Public access)
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        user = User.login(data.get('email'), data.get('password'))
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'token': access_token, 'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }}), 200
    except ValueError:
        return jsonify({'error': 'Invalid email or password'}), 401

# Get All Users (Admin only)
@user_bp.route('/', methods=['GET'])

def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        output.append(user_data)
    return jsonify({'users': output})

# Get Single User (Admin or user’s own access)
@user_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(id)

    if current_user['role'] != 'admin' and current_user['id'] != user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None,
        'contact_number': user.contact_number,
        'address': user.address,
        'is_doctor': user.is_doctor,
        'specialty': user.specialty,
        'medical_history': user.medical_history,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(user_data)

# Update User (Admin or user’s own access)
@user_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(id)

    if current_user['role'] != 'admin' and current_user['id'] != user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    if data.get('password'):
        user.password_hash = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
    user.contact_number = data.get('contact_number', user.contact_number)
    user.address = data.get('address', user.address)
    user.is_doctor = data.get('is_doctor', user.is_doctor)
    user.specialty = data.get('specialty', user.specialty)
    user.medical_history = data.get('medical_history', user.medical_history)

    db.session.commit()

    return jsonify({'message': 'User updated successfully', 'user': {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    }})

# Delete User (Admin only)
@user_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}),200