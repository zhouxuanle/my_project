from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message='Hello from Flask!')

if __name__ == '__main__':
    app.run(debug=True)