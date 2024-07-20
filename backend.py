from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Increased to 50MB

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_file('frontend.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        try:
            content = file.read().decode('utf-8')
            return jsonify({'content': content})
        except UnicodeDecodeError:
            return jsonify({'error': 'File encoding not supported. Please use UTF-8.'}), 400
    return jsonify({'error': 'Invalid file type'}), 400

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large. Maximum file size is 50MB.'}), 413

if __name__ == '__main__':
    app.run(debug=True, port=2138)