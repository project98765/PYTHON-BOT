from flask import Flask, request, jsonify
import requests
import json
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)  # Set the logging level
logger = logging.getLogger(__name__)

# Facebook App Access Token (replace with your token)
ACCESS_TOKEN = '8532504230140290|vriVvrS7gZz4orSXFkoKMNnLZRI'  # Replace with your App Access Token

# Load configuration from config.json
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

config = load_config()
VERIFY_TOKEN = config['verify_token']  # Verify token from config.json

# Facebook Graph API base URL
FB_API_URL = 'https://graph.facebook.com/v17.0/me/messages'

# Load commands and replies from the JSON file
def load_commands():
    with open('commands.json', 'r') as file:
        return json.load(file)

# Function to verify webhook
@app.route('/webhook', methods=['GET'])
def verify():
    token_sent = request.args.get('hub.verify_token')
    if token_sent == VERIFY_TOKEN:
        logger.info('Webhook verified successfully.')
        return request.args.get('hub.challenge')
    logger.warning('Invalid verification token.')
    return 'Invalid verification token'

# Function to receive messages
@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.get_json()
    logger.info('Received data: %s', data)  # Log the received data

    if data['object'] == 'page':
        for entry in data['entry']:
            messaging = entry['messaging']
            for message_event in messaging:
                if 'message' in message_event:
                    sender_id = message_event['sender']['id']
                    message_text = message_event['message'].get('text')

                    if message_text:
                        logger.info('Received message from %s: %s', sender_id, message_text)
                        # Load commands and replies
                        commands = load_commands()

                        # Check if the message matches a command
                        response = commands.get(message_text.lower(), "Sorry, I didn't understand that command.")
                        logger.info('Sending response to %s: %s', sender_id, response)

                        # Send the appropriate response
                        send_message(sender_id, response)
    return 'Message received', 200

# Function to send message back to user
def send_message(recipient_id, message_text):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }

    response = requests.post(FB_API_URL + '?access_token=' + ACCESS_TOKEN, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        logger.error('Error sending message: %s', response.text)
    else:
        logger.info("Message sent to %s: %s", recipient_id, message_text)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
