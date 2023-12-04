# app.py
from flask import Flask, jsonify, request
from api_handler import get_distance

app = Flask(__name__)

@app.route('/get_distance', methods=['POST'])
def calculate_distance():
    data = request.get_json()
    current_location = data.get('current_location')
    target_location = data.get('target_location')

    result = get_distance(current_location, target_location)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
