
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os

# Import extensions
from livewell_app.extensions import db, bcrypt, migrate

# Import blueprints for the updated controllers
from livewell_app.controllers.user_controller import user_bp
from livewell_app.controllers.phone_controller import phone_bp
from livewell_app.controllers.sms_log_controller import sms_log_bp
from livewell_app.controllers.ussd_session_controllers import ussd_session_bp
from livewell_app.controllers.appointment__controller import appointment_bp
from livewell_app.controllers.medical_record_controller import medical_record_bp
from livewell_app.controllers.voice_call_log_controller import voice_call_log_bp
from livewell_app.controllers.doctors_controller import doctor_bp



# Import Africa's Talking functions
from livewell_app.africas_talking import send_sms, make_voice_call, initiate_ussd_session, handle_ussd_response
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    # Initialize database and extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Initialize JWTManager with secret key
    app.config['JWT_SECRET_KEY'] = '12345'  
    jwt = JWTManager(app)

    # Set token expiration time
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  

    # Import models to register them with SQLAlchemy
    from livewell_app.models import user, phone, sms_log, ussd_session, appointment, medical_record, voice_call_log

    # Register blueprints for each controller
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(phone_bp, url_prefix='/api/v1/phones')
    app.register_blueprint(sms_log_bp, url_prefix='/api/v1/sms-logs')
    app.register_blueprint(ussd_session_bp, url_prefix='/api/v1/ussd-sessions')
    app.register_blueprint(appointment_bp, url_prefix='/api/v1/appointments')
    app.register_blueprint(medical_record_bp, url_prefix='/api/v1/medical-records')
    app.register_blueprint(voice_call_log_bp, url_prefix='/api/v1/voice-call-logs')
    app.register_blueprint(doctor_bp, url_prefix='/api/v1/doctors')

    # Serve Swagger JSON file
    @app.route('/swagger.json')
    def serve_swagger_json():
        try:
            return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')
        except FileNotFoundError:
            return jsonify({"message": "Swagger JSON file not found"}), 404

    # Swagger UI configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "LiveWell App"}
    )
    app.register_blueprint(swaggerui_blueprint)

    @app.route('/')
    def home():
        return 'Welcome to LiveWell App!'

    # Route to send SMS
    @app.route('/send-sms', methods=['POST'])
    @jwt_required()
    def send_sms_route():
        data = request.get_json()
        recipient = data.get('recipient')
        message = data.get('message')
        response = send_sms(recipient, message)
        return jsonify(response), 200 if response else 500

    # Route to make a voice call
    @app.route('/make-call', methods=['POST'])
    @jwt_required()
    def make_call_route():
        data = request.get_json()
        caller = data.get('caller')
        recipient = data.get('recipient')
        response = make_voice_call(caller, recipient)
        return jsonify(response), 200 if response else 500

    # Route to initiate USSD session
    @app.route('/start-ussd', methods=['POST'])
    @jwt_required()
    def start_ussd_route():
        data = request.get_json()
        phone_number = data.get('phone_number')
        ussd_code = data.get('ussd_code')
        response = initiate_ussd_session(phone_number, ussd_code)
        return jsonify(response), 200 if response else 500

    # Route to handle USSD responses
    @app.route('/ussd-response', methods=['POST'])
    def ussd_response_route():
        data = request.get_json()
        session_id = data.get('session_id')
        phone_number = data.get('phone_number')
        ussd_code = data.get('ussd_code')
        user_input = data.get('user_input')
        response = handle_ussd_response(session_id, phone_number, ussd_code, user_input)
        return jsonify(response), 200 if response else 500

    # Protected route example
    @app.route('/protected')
    @jwt_required()
    def protected():
        current_user_id = get_jwt_identity()
        return jsonify(logged_in_as=current_user_id), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
