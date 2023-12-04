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


# display score board -Su
@app.route('/score')
def get_score():
    sql = "SELECT * FROM scoreboard ORDER BY score DESC LIMIT 50"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(result)


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


# Creating a player based on name - Riina
@app.route('/create/<name>')
def create_name(name):
    co2_budget = 5000000
    co2_consumed = 0
    total_travelled = 0
    sql = f'''INSERT INTO player(player_name,co2_budget,co2_consumed,total_travelled)VALUES (%s,%s,%s,%s)'''
    cursor = connection.cursor(dictionary=True)
    val = (name, co2_budget, co2_consumed, total_travelled)
    cursor.execute(sql, val)
    cursor.fetchall()
    return {'Player': 'Created'}


# display plane types and info -Su
@app.route('/plane/<type>')
def get_plane_info(type):
    sql = f'''SELECT type, size, capacity, co2_emission_per_km, max_range FROM airplane WHERE type = %s
                '''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (type,))
    result = cursor.fetchone()
    return json.dumps(result)


# Reset player info, based on player_name - Riina
@app.route('/re_try/<name>')
def re_try(name):
    co2_budget = 5000000
    co2_consumed = 0
    total_travelled = 0
    sql = f'''UPDATE player SET co2_budget="{co2_budget}", co2_consumed="{co2_consumed}", total_travelled ="{total_travelled}" WHERE player_name ="{name}"'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    cursor.fetchall()
    return json.dumps({'Result': 'Updated'})


# check the host & port here
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)

