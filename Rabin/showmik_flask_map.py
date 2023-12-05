import mysql.connector
from flask import Flask, jsonify
from flask_cors import CORS

# Database connection settings
connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='test',
    user='root',
    password='1234',
    autocommit=True
)

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Route to get latitude and longitude by ICAO code
@app.route('/coordinates/<icao>')
def get_coordinates(icao):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident = %s"
    cursor.execute(query, (icao,))
    result = cursor.fetchone()
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Airport not found'}), 404

# check the host & port here
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
