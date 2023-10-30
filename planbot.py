from flask import Flask, request, redirect, jsonify
from flask_cors import CORS  # Import CORS
import json
import uuid
import logging
import requests  # Import requests for sending data to Zapier
from flask import make_response  # Import make_response

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)  # Initialize CORS

# Temporary in-memory storage for user data
user_data_store = {}

# Replace with the Zapier webhook URL you got
ZAPIER_WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/2850076/38e9im5/'

@app.route('/receive_data', methods=['POST'])
def receive_data():
    logging.info("POST data received: %s", request.form.to_dict())
    data = request.form.to_dict()
    token = str(uuid.uuid4())
    user_data_store[token] = data
    logging.info("Current user_data_store: %s", user_data_store)  # Log the current state

        # Send data to Zapier
        requests.post(ZAPIER_WEBHOOK_URL, json=data)

        # Your Softr HTML page URL here
        softr_url = "https://www.tpak.app/planbot-html"

        # Redirect with the token as a parameter
        intermediary_url = f"{softr_url}?token={token}"
        logging.info("Redirecting to: %s", intermediary_url)

        return redirect(intermediary_url, code=302)
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return jsonify({"error": "An error occurred"}), 500



@app.route('/get_data/<token>', methods=['GET'])
def get_data(token):
    logging.info("Fetching data for token: %s", token)
    data = user_data_store.get(token, {})
    return jsonify(data)

if __name__ == '__main__':
    app.run()
