from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os
import logging

# Set up logging for better debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/netaasreedb"
mongo = PyMongo(app)
CORS(app)

# Create the uploads folder if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# User Registration
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'msg': 'Missing username or password'}), 400
        password_hash = generate_password_hash(data['password'])
        user = {'username': data['username'], 'password': password_hash}
        mongo.db.users.insert_one(user)
        return jsonify({'msg': 'User registered successfully'}), 201
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        return jsonify({'msg': 'Error registering user'}), 500

# User Authentication
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'msg': 'Missing username or password'}), 400
        user = mongo.db.users.find_one({'username': data['username']})
        if user and check_password_hash(user['password'], data['password']):
            return jsonify({'msg': 'Login successful'}), 200
        return jsonify({'msg': 'Invalid credentials'}), 401
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        return jsonify({'msg': 'Error logging in'}), 500

# Upload File
@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'msg': 'No file part'}), 400
        file = request.files['file']
        
        # Limit file size (e.g., 10 MB)
        if file and file.mimetype in ['image/jpeg', 'image/png', 'application/pdf']:  # You can add more file types
            filename = file.filename
            file.save(os.path.join('uploads', filename))

            # Save file information to the database
            mongo.db.files.insert_one({'filename': filename, 'permissions': 'read-write'})
            return jsonify({'msg': 'File uploaded successfully'}), 201
        else:
            return jsonify({'msg': 'Invalid file type or file too large'}), 400
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return jsonify({'msg': 'Error uploading file'}), 500

if __name__ == '__main__':
    app.run(debug=True)
