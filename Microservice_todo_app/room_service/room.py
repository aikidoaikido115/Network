from flask import Flask, request, jsonify
from models import Room, db_session

app = Flask(__name__)

@app.route('/add/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    room = Room(user_id=data['user_id'], room_name=data['room_name'])
    db_session.add(room)
    db_session.commit()
    return jsonify({'id': room.id, 'user_id': room.user_id, 'room_name': room.room_name}), 201

@app.route('/query/rooms/<int:room_id>', methods=['GET'])
def read_room(room_id):
    room = db_session.query(Room).filter(Room.id == room_id).first()
    if room:
        return jsonify({'id': room.id, 'user_id': room.user_id, 'room_name': room.room_name})
    else:
        return jsonify({'error': 'Room not found'}), 404

@app.route('/remove/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = db_session.query(Room).filter(Room.id == room_id).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404
    db_session.delete(room)
    db_session.commit()
    return jsonify({"message": "Room deleted successfully"}), 200
        

if __name__ == '__main__':
    app.run(port=5003,debug=True)


#ลองเทส api ตั้งแต่อันแรกสุดด้วย