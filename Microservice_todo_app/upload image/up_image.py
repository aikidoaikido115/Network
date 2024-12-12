from flask import Flask, request, jsonify
from models import Image, db_session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add/image', methods=['POST'])
def upload_image():
    user_id = request.form.get('user_id')
    file = request.files.get('file')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    if not file or file.filename == '':
        return jsonify({'error': 'No file provided or no filename'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format. Allowed formats: png, jpg, jpeg, gif'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    image = Image(user_id=user_id, filename=filename)
    db_session.add(image)
    db_session.commit()

    return jsonify({
        'image_id': image.id,
        'user_id': image.user_id,
        'filename': image.filename,
        'message': 'Image uploaded successfully!'
    }), 201

@app.route('/query/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = db_session.query(Image).filter(Image.id == image_id).first()
    if not image:
        return jsonify({'error': 'Image not found'}), 404

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found on the server'}), 404

    return jsonify({
        'image_id': image.id,
        'user_id': image.user_id,
        'filename': image.filename,
        'image_url': filepath
    }), 200

if __name__ == '__main__':
    app.run(port=5005, debug=True)
