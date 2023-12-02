import mysql.connector
from flask import Flask
from flask_cors import CORS
import json

# check your setting
connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game_team12_mysql',
    user='root',
    password='riinaaal',
    autocommit=True
)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Sending all data of the player (if found multiple names by re-try, only the highest id will show.)
@app.route('/<name>')
def get_player_info(name):
    sql = f'''SELECT * from player where player_name = %s ORDER BY id DESC'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    return json.dumps(result)

# finding existing player_name -Su
@app.route('/player/<name>')
def get_player_name(name):
    sql = f'''SELECT player_name from player where player_name = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    return json.dumps(result)


# display plane types and info -Su
@app.route('/plane/<type>')
def get_plane_info(type):
    sql = f'''SELECT type, size, capacity, co2_emission_per_km, max_range FROM airplane WHERE type = %s
                '''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (type,))
    result = cursor.fetchone()
    return json.dumps(result)


# Create new player in database with same player_name as used before for re-try
@app.route('/re_try/<name>')
def re_try(name):
    co2_budget = 5000000
    co2_consumed = 0
    total_travelled = 0
    sql = f'''INSERT INTO player(player_name,co2_budget,co2_consumed,total_travelled)VALUES (%s,%s,%s,%s)'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (name, co2_budget, co2_consumed,total_travelled))
    cursor.fetchall()
    result = {"Result": "Re-try player created"}
    return json.dumps(result)


# check the host & port here
if __name__ == '__main__':
    app.run(use_reloader = True, host= '127.0.0.1', port = 3000)

