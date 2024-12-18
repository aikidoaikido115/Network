from flask import Flask, request, jsonify
from models import Image, db_session
import os
import urllib
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

# Helper function to sanitize the filename
def secure_filename_from_url(url):
    filename = url.split('/')[-1]  # Extract filename from URL
    return secure_filename(filename)

@app.route('/add/image', methods=['POST'])
def upload_image():
    user_id = request.json.get('user_id')  # Expecting JSON format in the request
    image_url = request.json.get('image_url')  # URL of the image to upload

    # Check if user_id and image_url are provided
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    if not image_url:
        return jsonify({'error': 'image_url is required'}), 400

    # Sanitize the filename and save the image from the URL
    filename = secure_filename_from_url(image_url)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Download and save the image to the server
    try:
        urllib.request.urlretrieve(image_url, filepath)
    except Exception as e:
        return jsonify({'error': f'Error downloading the image: {str(e)}'}), 500

    # Store the image information in the database
    image = Image(user_id=user_id, filename=filename)
    db_session.add(image)
    db_session.commit()

    # Return the image details in the response
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

    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found on the server'}), 404

    return jsonify({
        'image_id': image.id,
        'user_id': image.user_id,
        'filename': image.filename,
        'image_url': filepath
    }), 200

@app.route('/delete/image/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    # Ensure UPLOAD_FOLDER is set
    if 'UPLOAD_FOLDER' not in app.config:
        return jsonify({'error': 'UPLOAD_FOLDER is not configured'}), 500

    # Find the image by ID in the database
    image = db_session.query(Image).filter(Image.id == image_id).first()
    if not image:
        return jsonify({'error': 'Image not found'}), 404

    # Construct the file path
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

    try:
        # Delete the file from the filesystem if it exists
        if os.path.exists(filepath):
            os.remove(filepath)

        # Remove the image record from the database
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
