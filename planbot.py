from flask import Flask, request, redirect, jsonify
import json
import uuid
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Temporary in-memory storage for user data
user_data_store = {}

@app.route('/receive_data', methods=['POST'])
def receive_data():
    logging.info("POST data received: %s", request.form.to_dict())
    data = request.form.to_dict()
    token = str(uuid.uuid4())
    user_data_store[token] = data
    
    # Provided chatbot URL
    chatbot_url = "https://chat-app-fa81b9.zapier.app/"
    
    # Redirect with the token as a parameter
    intermediary_url = f"{chatbot_url}?token={token}"
    logging.info("Redirecting to: %s", intermediary_url)
    
    return redirect(intermediary_url, code=302)

@app.route('/get_data/<token>', methods=['GET'])
def get_data(token):
    logging.info("Fetching data for token: %s", token)
    data = user_data_store.get(token, {})
    return jsonify(data)

if __name__ == '__main__':
    app.run()
