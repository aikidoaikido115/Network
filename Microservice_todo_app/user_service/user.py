from flask import Flask, request, jsonify
from models import User, db_session

app = Flask(__name__)

@app.route('/create/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'username and password are required'}), 400
    
    user = User(username=data['username'], password=data['password'])
    db_session.add(user)
    db_session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201


@app.route('/auth/users', methods=['POST'])
def auth():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'username and password are required'}), 400

    user = db_session.query(User).filter_by(username=data['username']).first()


    if user and user.password == data['password']:

        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db_session.query(User).filter(User.id == user_id).first()
    if user:
        return jsonify({'id': user.id, 'username': user.username})
    else:
        return jsonify({'error': 'User not found'}), 404
    

#url อย่ามี _ คั่น
@app.route('/info', methods=['GET'])
def get_all_user():
    users = db_session.query(User).all() 
    if users:
        users_data = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(users_data)
    else:
        return jsonify({'error': 'User not found'}), 404
    

#เพิ่มฟีเจอร์ รูปโปรไฟล์

if __name__ == '__main__':
    app.run(port=5001, debug=True)
