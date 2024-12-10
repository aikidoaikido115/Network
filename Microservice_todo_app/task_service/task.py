from flask import Flask, request, jsonify
from models import Task, db_session
import requests
import json

app = Flask(__name__)

@app.route('/add/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(user_id=data['user_id'], description=data['description'], room_id=data['room_id'])
    db_session.add(task)
    db_session.commit()
    return jsonify({'id': task.id, 'user_id': task.user_id, 'description': task.description, 'room_id': task.room_id}), 201

@app.route('/query/tasks/<int:task_id>', methods=['GET'])
def read_task(task_id):
    task = db_session.query(Task).filter(Task.id == task_id).first()
    if task:
        return jsonify({'id': task.id, 'user_id': task.user_id, 'description': task.description, 'room_id': task.room_id})
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/remove/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = db_session.query(Task).filter(Task.id == task_id).first()
    print(task.description)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db_session.delete(task)
    db_session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200


@app.route('/llm/query/tasks/<int:user_id>', methods=['GET'])
def read_task_for_llm(user_id):
    task = db_session.query(Task).filter(Task.user_id == user_id).all() #ดึง task มาหมด


    if task:
        all_data = []
        for t in task:
            User_id = t.__dict__['user_id']
            id = t.__dict__['id']
            description = t.__dict__['description']
            room_id = t.__dict__['room_id']

            #ดึง room_name มา
            r = requests.get(f'http://localhost:5003/query/rooms/{room_id}')
            room_name = json.loads(r.text)["room_name"]
            # print(json.loads(r.text)["room_name"])

            data = {"user_id":User_id, "id":id, "description": description, "room_id":room_id, "room_name":room_name}
            all_data.append(data)


        # if task:
        #     return jsonify({'id': task.id, 'user_id': task.user_id, 'description': task.description, 'room_id': task.room_id})
        # else:
        #     return jsonify({'error': 'Task not found'}), 404
        return all_data, 201
    else:
        # message = json.dumps({'error': 'Task not found'})
        result = [{'error': 'Task not found'}]
        return result, 404
        

if __name__ == '__main__':
    app.run(port=5002,debug=True)


#ลองเทส api ตั้งแต่อันแรกสุดด้วย