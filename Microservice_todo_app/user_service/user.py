from flask import Flask, request, jsonify
from models import User, db_session

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    data = {'username': 'Misha1234'}
    user = User(username=data['username'])
    db_session.add(user)
    db_session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db_session.query(User).filter(User.id == user_id).first()
    if user:
        return jsonify({'id': user.id, 'username': user.username})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=5001)
