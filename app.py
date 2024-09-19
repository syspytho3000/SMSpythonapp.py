from flask import Flask, request, jsonify
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def index():
    return "Welcome to the SMS Sender API! Use the /send_sms endpoint to send messages."

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    message_body = data.get('message')
    to_number = data.get('to')

    if not message_body or not to_number:
        return jsonify({'error': 'Message and recipient number are required!'}), 400

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return jsonify({'success': True, 'sid': message.sid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
