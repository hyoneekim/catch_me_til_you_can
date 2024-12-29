# Fly me 'til you can! - Flight Simulator Game ✈️🌍

## Overview

**Fly me 'til you can!** is an exciting Python-based flight simulator game where players travel to various locations around the world, all while managing their CO2 emissions. The game challenges players to make strategic decisions regarding their flight choices, taking into account the CO2 impact of each destination and airplane type.

As players progress, they will encounter random events during their journey that could affect their flight path or emissions. The objective is to travel as far as possible without running out of CO2. Players can also compete for the highest score in a global leaderboard.

This game is built using **Python**, **Flask**, and **MariaDB** for a dynamic, interactive experience.

## Features

- **Dynamic Gameplay**: Players choose destinations to fly to, with each location and airplane type affecting CO2 emissions.
- **CO2 Management**: Players must manage their remaining CO2 wisely, as their choices determine how far they can travel.
- **Random Events**: Unpredictable events like weather changes or mechanical failures add excitement and challenge during the game.
- **Global Leaderboard**: A scoreboard allows players to compare their performance with others based on how far they can travel.
- **Continuous Database Interaction**: The game fetches and updates player data and locations using **MariaDB**.

## Technology Stack

- **Python**: Primary programming language used to build the game.
- **Flask**: Web framework to build the game’s back-end logic and server.
- **MariaDB**: Database to store location data, player scores, and game-related information.
- **HTML/CSS/JS**: For basic web interaction and displaying the game interface.

## How It Works

1. **Gameplay Mechanics**:
   - Players are tasked with flying to various locations, each with a unique CO2 cost, determined by the airplane type and distance.
   - Random events happen during the journey that could affect the gameplay, such as bad weather or technical problems.
   - The game continues as long as the player has enough CO2 to travel to the next destination.

2. **Scoring System**:
   - Players receive points based on the number of locations they can travel to before running out of CO2.
   - A leaderboard is maintained so players can compare their scores with others.

3. **Database Interaction**:
   - The game constantly interacts with a MariaDB database to fetch location data (including CO2 costs, names, etc.) and update the player's score.
   - Data such as the locations, available flights, and event occurrences are fetched and updated dynamically during the game.

## Demo Video 🎬

Watch the game in action in this demo video:

[Fly me 'til you can! - Demo](https://www.dropbox.com/scl/fi/puq1doopwvv9qmtfzk12z/game_demo.mov?rlkey=bpz7431a1xqjuyxsonj16zmma&st=sf7v3ptb&dl=0)
