import mysql.connector

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='team12',
         user='root',
         password='riinaaal12345',
         autocommit=True)


# BACKEND functions start here ----------------
def get_airport_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM airport
                  WHERE ident = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

#Riina's code
def create_player():

    while True:
        name = input("Enter name: ")

        sql = f"SELECT player_name FROM player WHERE player_name = '{name}' "
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        if cursor.rowcount == 0:
            co2_budget = 5000000
            co2_consumed = 0
            total_travelled = 0
            sql2 = f"INSERT INTO player(player_name,co2_budget,co2_consumed,total_travelled)VALUES (%s,%s,%s,%s)"
            val = [name, co2_budget, co2_consumed, total_travelled]
            cursor = connection.cursor()
            cursor.execute(sql2, val)
            cursor.fetchall()
            break

        else:
            print("Player already exists!")

    print(f"\nWelcome traveller, {name}! ")

    return name

# Rabin's code (modified)
def show_and_choose_airplane(userid):
    mycursor = connection.cursor()
    mycursor.execute("select type, size, capacity, co2_emission_per_km, max_range FROM airplane")
    results = mycursor.fetchall()

    print("Please choose your airplane: ")
    for idx, row in enumerate(results, start = 1):
        print(f"{idx}. {row[0]}")

    choice = int(input("Your choice?(1-4): "))
    if choice == 1:
        sql = f"UPDATE choice SET plane_type = 'large_airport' WHERE player_name = '{userid}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        return 'large_airport'
    elif choice == 2:
        sql = f"UPDATE choice SET plane_type = 'medium_airport' WHERE player_name = '{userid}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        return 'medium_airport'
    elif choice ==3:
        sql = f"UPDATE choice SET plane_type = 'heliport' WHERE player_name = '{userid}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        return 'heliport'
    elif choice == 4:
        sql = f"UPDATE choice SET plane_type = 'small_airport' WHERE player_name = '{userid}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        return 'small_airport'


def calculate_distance(current, target):
    from geopy import distance

    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km


def get_userdata(userid):
    sql = f'''SELECT player_name, co2_budget, co2_consumed, total_travelled FROM player WHERE player_name = %s
                '''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (userid,))
    result = cursor.fetchone()
    return result

def left_budget(userid):
    data = get_userdata(userid)
    return data['co2_budget'] - data['co2_consumed']

counts = 4
def counterforloop(counts):
    counts -= 1
    return counts

def range_in (airplane_size, userid, turn):
    global airportCode, co2_emission, destination, chosenId, chosenDis, chosenCo2
    global counts

    sql4 = f'''SELECT current_location FROM player WHERE player_name = "{userid}"'''
    cursor = connection.cursor()
    cursor.execute(sql4)
    result = cursor.fetchone()
    current = result[0]

    sql = f'''SELECT ident, airport.name, airport.continent, country.name as country, airplane.max_range, airplane.co2_emission_per_km, airplane.capacity
            FROM airport 
            INNER JOIN airplane on (airplane.size = airport.type)
            INNER JOIN country on (airport.iso_country = country.iso_country)
            WHERE airport.type = '{airplane_size}' ORDER BY RAND () LIMIT 5'''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    print("\nHere are possible destinations you can choose!\n")
    print("num| continent |  country  |      airport      |  distance  | expected co2 emission")
    print("-----------------------------------------")

    if cursor.rowcount >= 1:
        destination = list()
        index_counter = 1
        for row in result:
            airportCode = row[0]
            range = row[4]
            distance = calculate_distance(current, airportCode)
            co2_emission = distance * row[4]/ row[5]
            destination.append((airportCode, round(distance), round(co2_emission)))
            if (range <= distance) or (co2_emission >= left_budget(userid)):
                destination.pop()
            else:

                print(f"{index_counter}  |  {row[2]}    | {row[3]} | {row[1]} | {round(distance)} km | {round(co2_emission)}")
                index_counter += 1
    print("\nIf there isn't any destination shown, try another plane. You'll go back by hitting enter.")
    print("BUT REMEMBER, you can change the plane only 3 times!") # counting doesn't work at the moment: while loop <-> range_in() crash
    choice_input = input("\nWhere do you want to travel? Type the number or enter: \n")
    while counts > 0:
        if choice_input == "":
            counts = counterforloop(counts)
            if counts > 0:
                print(f"attempts left : {counts - 1} \n")
                airplane = show_and_choose_airplane(userid)
                range_in(airplane, userid, turn)
                break
            elif counts == 0:
                print(f"attempts left : {counts} \n")
                print("Oh no, you can't change your plane anymore. This means your game is OVER!!")
                game_over_and_save(userid)
                break
        else:
            choice = int(choice_input)
            if 1 <= choice <= len(destination):
                chosen = destination[choice-1]
                chosenId = chosen[0]
                chosenDis = chosen[1]
                chosenCo2 = chosen[2]
                #print(chosen)

                sql3 = f"UPDATE choice SET co2_spent = {chosenCo2}, distance_km = {chosenDis} WHERE (turn = {turn} AND player_name = '{userid}')"

                cursor = connection.cursor()
                cursor.execute(sql3)

                sql5 = f'''UPDATE player SET current_location = '{chosenId}' WHERE player_name = "{userid}"'''
                cursor = connection.cursor()
                cursor.execute(sql5)
                break



def event_occurrence(turn,userid):
    import random
    sql = f"SELECT * from event"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    random.choice(result)
    weights = []
    events = []
    for row in result:
        #print(row)
        events.append(row[1])
        weights.append(row[3]*100)

    #print(weights)
    pick = random.choices(events, weights = weights, k=1)

    posneg = ''
    co2 = 0
    event = 0
    sql = f"SELECT * from event WHERE info = '{pick[0]}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result2 = cursor.fetchall()
    for row in result2:
        posneg = row[2]
        co2 = row[4]
        event = row[0]

    if pick[0] == 'No event':
        print("")
        sql2 = f"UPDATE choice SET event_occurred = {event} WHERE turn = {turn} AND player_name = '{userid}'"
        cursor = connection.cursor()
        cursor.execute(sql2)
    else:
        print("\n\nyou've got a message from control tower!")
        print(pick[0])
        print("\nThe event will affect your flight :")
        if posneg == 'neg':
            #if row[5] == 'NULL': ignoring the distance pe
            print(f"Co2 consumption is {co2 * 100}% increased!")
            sql3 = f"UPDATE choice SET event_occurred = {event}, co2_spent = co2_spent - co2_spent* {co2} WHERE turn = {turn} AND player_name = '{userid}'"
            cursor = connection.cursor()
            cursor.execute(sql3)
        elif posneg == 'pos':
            print(f"Co2 consumption is {co2 * 100}% decreased!")
            sql4 = f"UPDATE choice SET event_occurred = {event}, co2_spent = co2_spent - co2_spent* {co2} WHERE turn = {turn} AND player_name = '{userid}'"
            cursor = connection.cursor()
            cursor.execute(sql4)

def update_turn_data(turn, userid):
    global dis, co2
    sql = f'''SELECT distance_km, co2_spent from choice where turn = {turn} and player_name = "{userid}"'''
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        dis = row[0]
        co2 = row[1]
    sql2 = f'''UPDATE player SET co2_consumed = co2_consumed + {co2}, total_travelled = total_travelled + {dis} WHERE player_name = "{userid}"'''
    cursor = connection.cursor()
    cursor.execute(sql2)


def condition_checker(userid):
    global co2_budget, co2_consumed

    sql = f"SELECT co2_budget, co2_consumed FROM player WHERE player_name = '{userid}'"

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount == 1:
        for row in result:
            co2_budget = row[0]
            co2_consumed = row[1]
    co2_left = co2_budget - co2_consumed
    if co2_left <= 0:
        return game_over_and_save(userid)
    else:
        return

def end_display():

    exit_process = True

    while exit_process:
        toScoreboard = input("Do you want to go check score board? (y/n) : ")
        if toScoreboard == 'y':
            show_scoreboard()
            toFrontPage = input("By hitting enter, you'll go back to the front page.: ")
            if toFrontPage == '':
                return front_display()
            exit_process = False
        elif toScoreboard == 'n':
            toFrontPage = input("By hitting enter, you'll go back to the front page.: ")
        if toFrontPage == '':
            return front_display()
        else:
            print("Invalid answer. Try again.")


def game_over_and_save(userid):
    global name, score
    sql1 = f"SELECT player_name, total_travelled FROM player WHERE (co2_budget >= co2_consumed) AND (player_name = '{userid}')"
    #print(sql1)
    cursor = connection.cursor()
    cursor.execute(sql1)
    result = cursor.fetchall()
    if cursor.rowcount == 1:
        for row in result:
            print(f"{row[0]}, You cannot fly with the remaining budget anywhere. GAME OVER!")
            name = row[0]
            score = row[1]
    save = input("Do you want to save your score in score board? (y/n): ")
    if save == 'y':
        sql2 = f"INSERT INTO scoreboard (player_name, score) VALUES (%s, %s)"
        val = [name, score]
        cursor = connection.cursor()
        cursor.execute(sql2, val)
        print(f"your userid <{name}> and your score <{score}> has been saved in the scoreboard.")
    return end_display()

def show_scoreboard():
    sql = "SELECT * FROM scoreboard ORDER BY score DESC LIMIT 50"
    #print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        print(f"<<<SCORE BOARD>>>")
        print(f"Player      | score")
        print(f"--------------------------")
        for row in result:
            print(f"{row[1]} | {row[2]}")
        return

def show_panel(userid):
    global current
    sql1 = f"SELECT co2_budget, co2_consumed, total_travelled, current_location FROM player where player_name = '{userid}'"
    cursor = connection.cursor()
    cursor.execute(sql1)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            current = row[3]
            print("<<Your status>>")
            print("-------------------------------------")
            print(f"|co2_budget              | {row[0]}|")
            print(f"|co2_consumed            | {row[1]}|")
            print(f"|total distance travelled| {row[2]}|")
            print("-------------------------------------")
    sql2 =f"SELECT name from airport where ident= '{current}'"
    cursor = connection.cursor()
    cursor.execute(sql2)
    result = cursor.fetchone()
    print(f"\nYour current location is {result[0]}.")
    return

# FRONT END(ish) FUNCTIONS & CODES START HERE-------------------
def main_display(userid):
    global turn
    main_processing = True
    while main_processing:
        sql1 = f"SELECT COUNT(player_name) FROM choice WHERE player_name = '{userid}'"
        cursor = connection.cursor()
        cursor.execute(sql1)
        result = cursor.fetchall()
        if cursor.rowcount == 1:
            for row in result:
                turn = row[0] +1
                print(f"ROUND {turn}")
                print("\n")

        sql2 = f"INSERT INTO choice (turn, player_name) VALUES(%s,%s) "
        val2 = [turn,userid]
        cursor = connection.cursor()
        cursor.execute(sql2,val2)
        show_panel(userid)
        #condition_checker(userid)

        # game_over_and_save activated ==> go to end_display func.

        airplane = show_and_choose_airplane(userid)
        range_in(airplane,userid,turn)

        if counts -1 >= 0:
            print("\n\n You're flying up in the air...")
            event_occurrence(turn,userid)
            print("\n\n Now your plane is landing....")
            update_turn_data(turn,userid)
        else:
            return


    return


def front_display():
    initial = True
    while initial:
        print("----------------------")
        print("| FLY ME,            |")
        print("|      'TIL YOU CAN! |")
        print("----------------------")
        print("\n")
        print("1: START A NEW GAME")
        print("2: CHECK TUTORIAL")
        print("3: SCORE BOARD")
        print("4: QUIT")
        print("\n")

        command = int(input("Enter your command: "))
        if command == 1:
            print("Your adventure is about to start,")
            name = create_player()
            print("Your journey begins at Helsinki-Vantaa airport, Finland.\n")
            initial = False

            main_display(name)

        elif command == 2:
            print("<<TUTORIAL>>")
            print("\n")
            print("You're going to travel across the world by choosing a flight.")
            print("Your GOAL is to travel as far as you can go with your limited co2 budget!")
            print("The game ends when you have spent all the budget and can't go anywhere anymore.")
            print("Good luck!")
            print("\n")
            print("Going back to the front page...")
            print("\n")

        elif command == 3:
            show_scoreboard()
            print("\n")
            print("Going back to the front page....")
            print("\n")
            print("\n")
        elif command == 4:
            print("Bye bye!")
            initial = False
        else:
            print("Invalid command. Please try again!")




#GAME STARTS HERE =====================
front_display()