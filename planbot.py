from flask import Flask, request, redirect
import json
import uuid
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Temporary storage for user data
user_data_store = {}

@app.route('/receive_data', methods=['POST'])
def receive_data():
    logging.info("POST data received: %s", request.form.to_dict())
    data = request.form.to_dict()
    token = str(uuid.uuid4())
    user_data_store[token] = data
    intermediary_url = f"https://your-intermediary-page.com/?token={token}"
    logging.info("Redirecting to: %s", intermediary_url)
    return redirect(intermediary_url)

@app.route('/get_data/<token>', methods=['GET'])
def get_data(token):
    logging.info("Fetching data for token: %s", token)
    return json.dumps(user_data_store.get(token, {}))

if __name__ == '__main__':
    app.run(debug=True)

