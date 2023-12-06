import mysql.connector
from flask import Flask, request
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

# getting location and airport names for display in main.html -Su
@app.route('/coord')
def get_coordinates():
    sql = f'''SELECT name, iso_country, latitude_deg, longitude_deg
FROM airport
INNER JOIN player ON airport.ident = player.current_location
WHERE player.id = (SELECT MAX(id) FROM player)
'''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return json.dumps(result)

@app.route('/destination/<size>')
def get_destination(size):
    sql = f'''SELECT ident, latitude_deg, longitude_deg, airport.name, airport.continent, country.name as country, airplane.max_range, airplane.co2_emission_per_km, airplane.capacity
                FROM airport 
                INNER JOIN airplane on (airplane.size = airport.type)
                INNER JOIN country on (airport.iso_country = country.iso_country)
                WHERE airport.type = '{size}' ORDER BY RAND () LIMIT 5'''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(result)


@app.route('/current/<userid>')  # getting current icao code the lat & lon info of the airport
def get_current(userid):
    sql = f'''SELECT p.current_location, a.latitude_deg, a.longitude_deg, co2_budget, co2_consumed
                FROM player p
                JOIN airport a ON p.current_location = a.ident
                WHERE p.player_name = "{userid}"'''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return json.dumps(result)


# sending the result data back to JS to display the info -su
@app.route('/result/<turn>/<userid>')
def get_result(turn, userid):
    # placeholder user id and turn
    sql = f'''SELECT distance_km, co2_spent from choice WHERE turn ={turn} AND player_name = "{userid}"'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    return json.dumps(result)


# fetching event occurrence data from JS & updating DB -Su
@app.route('/result', methods=['post'])
def receive_pick():
    data = request.json
    received_pick = data.get('pick')

    # placeholder user id and turn
    turn = 1
    userid = 'su'

    if received_pick[2] == 'NULL':
        sql = f"UPDATE choice SET event_occurred = {received_pick[0]} WHERE turn = {turn} AND player_name = '{userid}'"
        cursor = connection.cursor()
        cursor.execute(sql)

    else:

        if received_pick[2] == 'neg':
            sql2 = f"UPDATE choice SET event_occurred = {received_pick[0]}, co2_spent = co2_spent + co2_spent * {received_pick[4]} WHERE turn = {turn} AND player_name = '{userid}'"
            cursor = connection.cursor()
            cursor.execute(sql2)

        elif received_pick[2] == 'pos':
            sql3 = f"UPDATE choice SET event_occurred = {received_pick[0]}, co2_spent = co2_spent - co2_spent * {received_pick[4]} WHERE turn = {turn} AND player_name = '{userid}'"
            cursor = connection.cursor()
            cursor.execute(sql3)

    return json.dumps({'Result': 'Updated'})


# fetch event data -Su
@app.route('/event')
def get_event():
    sql = f"SELECT * from event"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(result)


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


# Get player info to display - Su did JS part Riina rest
@app.route('/current')
def get_data():
    sql = f'''SELECT * FROM player WHERE id = (SELECT MAX(id) FROM player)'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
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

    sql2 = f'''INSERT INTO choice (turn, player_name)VALUES(%s,%s)'''
    val = (0, name)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql2, val)
    cursor.fetchall()
    return {'Player': 'Created'}


# Create round and send back round number - Riina
@app.route('/round')
def get_round():
    # Get player name
    sql = f'''SELECT player_name FROM player WHERE id = (SELECT MAX(id) FROM player)'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result1 = cursor.fetchall()
    name = ''
    for names in result1:
        name = names['player_name']

    # Get current turn
    sql2 = f'''SELECT turn FROM choice WHERE player_name = "{name}" AND turn = (SELECT MAX(turn) FROM choice WHERE player_name = "{name}")'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql2)
    result2 = cursor.fetchall()

    turn = 0
    for numb in result2:
        turn = int(numb['turn'])
    # Insert new turn
    current = turn + 1
    sql4 = f'''INSERT INTO choice (turn, player_name)VALUES(%s, %s) '''
    val = (current, name)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql4, val)
    cursor.fetchall()
    return json.dumps(current)


# display plane types and info -Su
@app.route('/plane/<type>')
def get_plane_info(type):
    sql = f'''SELECT type, size, capacity, co2_emission_per_km, max_range FROM airplane WHERE type = %s '''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (type,))
    result = cursor.fetchone()
    return json.dumps(result)


# get plane choice and update to choice table - Riina
@app.route('/choose/<plane>')
def enter_choice(plane):
    sql = f''' SELECT player_name FROM player WHERE  player_name = (SELECT player_name FROM player WHERE id = (SELECT MAX(id) FROM player))'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result1 = cursor.fetchall()
    name = ''
    for names in result1:
        name = names['player_name']

    sql2 = f'''UPDATE choice SET plane_type = "{plane}" WHERE player_name = "{name}" AND turn = (SELECT MAX(turn) FROM choice WHERE player_name = "{name}") '''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql2)
    cursor.fetchall()
    return json.dumps({'Info': 'Updated'})


# Get co2_budget of player - Riina
@app.route('/co2_budget')
def get_co2_budget():
    sql = f'''SELECT co2_budget FROM player WHERE id = (SELECT MAX(id) FROM player)'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(result)


# Get airport, co2_spent and distance. Update info to choice and location to player current location - Riina
@app.route('/<airport>/<co2_spent>/<distance>')
def update_co2_etc_info(airport, co2_spent, distance):
    # Get player name
    sql = f'''SELECT player_name FROM player WHERE id = (SELECT MAX(id) FROM player)'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result1 = cursor.fetchall()
    name = ''
    for names in result1:
        name = names['player_name']

    # Get current turn
    sql2 = f'''SELECT turn FROM choice WHERE player_name = "{name}" AND turn = (SELECT MAX(turn) FROM choice WHERE player_name = "{name}")'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    turn = 0
    for numb in result2:
        turn = int(numb['turn'])

    # Get airports ICAO code based on airport name
    sql3 = '''SELECT ident FROM airport WHERE name LIKE  %s '''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql3, (airport,))
    result3 = cursor.fetchall()
    icao = ''
    for loc in result3:
        icao = loc['ident']

    # Update co2_spent and distance to choice
    sql4 = f'''UPDATE choice SET co2_spent = "{co2_spent}", distance_km = "{distance}" WHERE player_name = "{name}" AND turn = "{turn}"'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql4)
    cursor.fetchall()

    # Update player location
    sql5 = f'''UPDATE player SET current_location = "{icao}" WHERE player_name = "{name}"'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql5)
    cursor.fetchall()

    return json.dumps({'Info': 'Updated'})


# Reset player info, based on player_name - Riina
@app.route('/re_try')
def re_try():
    sql = f'''SELECT player_name FROM player WHERE id = (SELECT MAX(id) FROM player)'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result1 = cursor.fetchall()
    name = ''
    for names in result1:
        name = names['player_name']

    co2_budget = 5000000
    co2_consumed = 0
    total_travelled = 0
    sql2 = f'''UPDATE player SET co2_budget="{co2_budget}", co2_consumed="{co2_consumed}", total_travelled ="{total_travelled}" WHERE player_name ="{name}"'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql2)
    cursor.fetchall()
    sql3 = f'''DELETE FROM choice WHERE player_name = "{name}"'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql3)
    cursor.fetchall()
    return json.dumps({'Result': 'Updated'})


# check the host & port here
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
