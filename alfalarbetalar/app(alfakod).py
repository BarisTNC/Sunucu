from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid request"}), 400

    print(f"Received message: {data['message']}")
    return jsonify({"response": f"Echo: {data['message']}"})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)