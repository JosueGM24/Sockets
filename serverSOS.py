from flask import Flask, request, jsonify, send_file, render_template, after_this_request
from flask_cors import CORS
import os
import zipfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
upload_dir = 'uploads'

# Crear el directorio de uploads si no existe
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(upload_dir)
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(upload_dir, filename))
    return jsonify({'message': 'File successfully uploaded'}), 201

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join(upload_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': 'File successfully deleted'}), 200
        else:
            return jsonify({'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_files():
    try:
        files = request.json.get('files', [])
        zip_path = os.path.join('files.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                file_path = os.path.join(upload_dir, file)
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
        
        @after_this_request
        def remove_file(response):
            try:
                os.remove(zip_path)
            except Exception as e:
                app.logger.error(f'Error removing or closing file handle: {e}')
            return response

        return send_file(zip_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5002)
