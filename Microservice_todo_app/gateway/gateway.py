from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    resp = requests.post(f'{USER_SERVICE_URL}/users', json=data)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(port=5000, debug=True)