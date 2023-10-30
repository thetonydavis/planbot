
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import logging
import requests
import uuid

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)  # Initialize CORS

# Temporary in-memory storage for user data
user_data_store = {}

# Replace with the Zapier webhook URL you got
ZAPIER_WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/2850076/38e9im5/'

@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        # Debugging Step 1: Log the incoming POST data
        logging.info("Debug Step 1: POST data received: %s", request.form.to_dict())
        
        data = request.form.to_dict()
        token = str(uuid.uuid4())
        user_data_store[token] = data

        # Debugging Step 2: Send data to Zapier and log it
        requests.post(ZAPIER_WEBHOOK_URL, json=data)
        logging.info("Debug Step 2: Data sent to Zapier: %s", data)
        
        # Your Softr HTML page URL here
        softr_url = "https://www.tpak.app/planbot-html"

        # Debugging Step 3: Prepare the redirect URL and log it
        intermediary_url = f"{softr_url}?token={token}"
        logging.info("Debug Step 3: Redirecting to: %s", intermediary_url)

        return redirect(intermediary_url, code=302)
    except Exception as e:
        # Debugging Step 4: Log any exceptions
        logging.error("Debug Step 4: An error occurred: %s", str(e))
        return jsonify({"error": "An error occurred"}), 500

@app.route('/get_data/<token>', methods=['GET'])
def get_data(token):
    # Debugging Step 5: Log the token and data being fetched
    logging.info("Debug Step 5: Fetching data for token: %s", token)
    data = user_data_store.get(token, {})
    return jsonify(data)

if __name__ == '__main__':
    app.run()
