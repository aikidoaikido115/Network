from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import json


load_dotenv()

app = Flask(__name__)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')
TASK_SERVICE_URL = os.getenv('TASK_SERVICE_URL')
ROOM_SERVICE_URL = os.getenv('ROOM_SERVICE_URL')
LLM_SERVICE_URL = os.getenv('LLM_SERVICE_URL')
UPIMG_SERVICE_URL=os.getenv('UPIMG_SERVICE_URL')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    res = requests.post(f'{USER_SERVICE_URL}/create/users', json=data)
    return jsonify(res.json()), res.status_code


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    res = requests.post(f'{USER_SERVICE_URL}/auth/users', json=data)
    return jsonify(res.json()), res.status_code


@app.route('/create/room', methods=["POST"])
def create_room():
    data = request.get_json()
    res = requests.post(f'{ROOM_SERVICE_URL}/add/rooms', json=data)
    return jsonify(res.json()), res.status_code

@app.route('/read/room/<int:room_id>', methods=["GET"])
def read_room(room_id):
    res = requests.get(f'{ROOM_SERVICE_URL}/query/rooms/{room_id}')
    return jsonify(res.json()), res.status_code

@app.route('/delete/room/<int:room_id>', methods=["DELETE"])
def delete_room(room_id):
    res = requests.delete(f'{ROOM_SERVICE_URL}/remove/rooms/{room_id}')
    return jsonify(res.json()), res.status_code


##################


@app.route('/create/task', methods=["POST"])
def create_task():
    data = request.get_json()
    res = requests.post(f'{TASK_SERVICE_URL}/add/tasks', json=data)
    return jsonify(res.json()), res.status_code

@app.route('/read/task/<int:task_id>', methods=["GET"])
def read_task(task_id):
    res = requests.get(f'{TASK_SERVICE_URL}/query/tasks/{task_id}')
    return jsonify(res.json()), res.status_code

@app.route('/delete/task/<int:task_id>', methods=["DELETE"])
def delete_task(task_id):
    res = requests.delete(f'{TASK_SERVICE_URL}/remove/tasks/{task_id}')
    return jsonify(res.json()), res.status_code

##################
@app.route('/add/image', methods=['POST'])
def add_image():
    data = request.get_json()
    res = requests.post(f'{UPIMG_SERVICE_URL}/add/image', json=data)
    return jsonify(res.json()), res.status_code

@app.route('/query/image/<int:image_id>', methods=['GET'])
def query_image(image_id):
    res = requests.get(f'{UPIMG_SERVICE_URL}/query/image/{image_id}')
    return jsonify(res.json()), res.status_code

@app.route('/delete/image/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    res = requests.delete(f'{UPIMG_SERVICE_URL}/delete/image/{image_id}')
    return jsonify(res.json()), res.status_code
##################

@app.route('/gemini', methods=["GET"])
def ask_gemini():
    json_body = request.get_json()
    # user_id = data.get('user_id')
    # prompt = data.get('prompt')
    try:
        # print(LLM_SERVICE_URL)
        # json_body = {"user_id": user_id}

        res = requests.get(f'{LLM_SERVICE_URL}/llm', json=json_body)
        data = json.loads(res.text)
        

        return data, res.status_code

    except requests.exceptions.RequestException as e:

        return jsonify({"error": "Failed to connect to LLM service", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)