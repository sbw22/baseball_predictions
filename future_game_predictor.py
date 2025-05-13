import numpy as np
import csv
from keras.models import load_model
import joblib
from joblib import load
import requests
import json
import statsapi
import datetime



def load_model_and_scaler():

    model = load_model(f'model_and_scalers/trained_strikeout_model.h5')

    strikeout_scaler = load('model_and_scalers/strikeout_scaler.pkl')

    input_scalers = joblib.load('model_and_scalers/input_scalers.pkl')

    return model, strikeout_scaler, input_scalers




def fetch_lineup_data():
    game_ids = []

    # Get today's date
    today = datetime.datetime.now()
    # Format the date as MM/DD/YYYY
    formatted_date = today.strftime("%m/%d/%Y")
    games = statsapi.schedule(start_date=f'{formatted_date}',end_date=f'{formatted_date}')

    for game in games:
        game_id = game.get("game_id")
        if game_id:
            game_ids.append(game_id)

    for game_id in game_ids:
        # Fetch the game data using the game ID
        game_data = statsapi.boxscore(game_id)
        print(f"game_data: {game_data}")
        break
        if game_data:
            return game_data


    print(f"Games: {games}")
    



def process_lineup_data(data):
    games = data.get("games", [])
    for game in games:
        away_team = game.get("away", {})
        home_team = game.get("home", {})

        # Extract away team pitcher info
        away_pitcher = away_team.get("pitcher", {})
        away_pitcher_name = away_pitcher.get("name")
        away_pitcher_era = away_pitcher.get("pitcherEra")

        # Extract home team pitcher info
        home_pitcher = home_team.get("pitcher", {})
        home_pitcher_name = home_pitcher.get("name")
        home_pitcher_era = home_pitcher.get("pitcherEra")

        # Extract away team lineup
        away_lineup = away_team.get("lineup", [])
        away_batters = [player.get("player") for player in away_lineup]

        # Extract home team lineup
        home_lineup = home_team.get("lineup", [])
        home_batters = [player.get("player") for player in home_lineup]

        # Process the extracted information as needed
        print(f"Away Team Pitcher: {away_pitcher_name}, ERA: {away_pitcher_era}")
        print(f"Away Team Batters: {away_batters}")
        print(f"Home Team Pitcher: {home_pitcher_name}, ERA: {home_pitcher_era}")
        print(f"Home Team Batters: {home_batters}")

    



def main():
    
    model, strikeout_scaler, input_scalers = load_model_and_scaler()

    year = 2025

    # rand_game_s = statsapi.game()

    # Get names of pitchers
    # Get the data for the pitchers
    # Get names of batters going up against the pitchers
    # Get the data for the batters
    # Process all the data
    # Pass proccessed data to the model

    data = fetch_lineup_data()
    if data:
        process_lineup_data(data)

    
    

if __name__ == "__main__":
    main()
