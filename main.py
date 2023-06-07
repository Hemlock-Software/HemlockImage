import os
import base64
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import *
from werkzeug.utils import secure_filename
import filetype

VERSION = "0.1.0"
ROOT_URL = "http://localhost:42069"

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/")
def index():
    return "HemlockImage Server<br>Version " + VERSION


@app.route("/api/v1/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        if filetype.is_image(file.stream.read(261)):
            file.stream.seek(0)  # reset file pointer to the start after reading
            filename = secure_filename(file.filename)
            random_str = base64.urlsafe_b64encode(os.urandom(15)).decode('utf-8')
            dir_path = os.path.join('static', 'images', random_str)
            os.makedirs(dir_path, exist_ok=True)
            file.save(os.path.join(dir_path, filename))
            return jsonify(file_url=ROOT_URL+f'/images/{random_str}/{filename}'), 200
        else:
            return jsonify(error="Uploaded file is not an image"), 400


@app.route('/images/<path:path>')
def serve_image(path):
    return send_from_directory('static/images', path)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=42069)
