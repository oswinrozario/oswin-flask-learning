from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def index():
  return jsonify({'message': 'Hello, World!'}), 200, {'Content-Type': 'application/json'} 
