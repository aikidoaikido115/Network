from flask import Flask, request, jsonify
from models import Image, db_session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


def secure_filename_from_url(url):
    filename = url.split('/')[-1]
    return secure_filename(filename)

@app.route('/add/image', methods=['POST'])
def upload_image():
    user_id = request.json.get('user_id')
    image_url = request.json.get('image_url')  

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    if not image_url:
        return jsonify({'error': 'image_url is required'}), 400


    filename = secure_filename_from_url(image_url)



    image = Image(user_id=user_id, filename=filename, image_url=image_url)
    db_session.add(image)
    db_session.commit()


    return jsonify({
        'image_id': image.id,
        'user_id': image.user_id,
        'filename': image.filename,
        'image_url': image_url,
        'message': 'Image uploaded successfully!'
    }), 201

@app.route('/query/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = db_session.query(Image).filter(Image.id == image_id).first()
    
    if not image:
        return jsonify({'error': 'Image not found'}), 404

    return jsonify({
        'image_id': image.id,
        'user_id': image.user_id,
        'filename': image.filename,
        'image_url': image.image_url
    }), 200

@app.route('/delete/image/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):

    image = db_session.query(Image).filter(Image.id == image_id).first()
    if not image:
        return jsonify({'error': 'Image not found'}), 404

    try:

        db_session.delete(image)
        db_session.commit()

        return jsonify({
            'message': f'Image with ID {image_id} has been successfully deleted.',
            'image_id': image_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5005, debug=True)
