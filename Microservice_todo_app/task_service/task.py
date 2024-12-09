from flask import Flask, request, jsonify
from models import Task, db_session

app = Flask(__name__)

@app.route('/add/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(user_id=data['user_id'], description=data['description'])
    db_session.add(task)
    db_session.commit()
    return jsonify({'id': task.id, 'user_id': task.user_id, 'description': task.description}), 201

@app.route('/query/tasks/<int:task_id>', methods=['GET'])
def read_task(task_id):
    task = db_session.query(Task).filter(Task.id == task_id).first()
    if task:
        return jsonify({'id': task.id, 'user_id': task.user_id, 'description': task.description})
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
        

if __name__ == '__main__':
    app.run(port=5002,debug=True)


#ลองเทส api ตั้งแต่อันแรกสุดด้วย