# africas_talking.py

import africastalking

# Initialize Africa's Talking credentials
username = "sandbox"  # Your Africa's Talking application username
api_key = "atsk_71a3e3a9743a9b82a7ecd5e0af30d23efaea820bdddc5a830de96305e0a7ac563c8336ea"  # Y88 our Africa's Talking API key

# Initialize the Africa's Talking client
africastalking.initialize(username, api_key)
sms = africastalking.SMS
voice = africastalking.Voice
ussd = africastalking.USSD

# Function to send SMS
def send_sms(recipient, message):
    try:
        response = sms.send(message, [recipient])
        return response
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None

# Function to initiate a voice call
def make_voice_call(caller, recipient):
    try:
        response = voice.call(caller, recipient)
        return response
    except Exception as e:
        print(f"Error making voice call: {e}")
        return None

# Function to initiate a USSD session
def initiate_ussd_session(phone_number, ussd_code):
    try:
        response = ussd.initiate(phone_number, ussd_code)
        return response
    except Exception as e:
        print(f"Error initiating USSD session: {e}")
        return None

# Function to handle USSD responses (e.g., user input during a USSD session)
def handle_ussd_response(session_id, phone_number, ussd_code, user_input):
    try:
        response = ussd.respond(session_id, phone_number, ussd_code, user_input)
        return response
    except Exception as e:
        print(f"Error handling USSD response: {e}")
        return None
