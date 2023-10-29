from flask import Flask, request, redirect
import json
import uuid

app = Flask(__name__)

# Temporary storage for user data
user_data_store = {}

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.form.to_dict()
    token = str(uuid.uuid4())
    user_data_store[token] = data
    intermediary_url = f"https://chat-app-fa81b9.zapier.app/?token={token}"
    return redirect(intermediary_url)

@app.route('/get_data/<token>', methods=['GET'])
def get_data(token):
    return json.dumps(user_data_store.get(token, {}))

if __name__ == '__main__':
    app.run(debug=True)
