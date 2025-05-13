import numpy as np
import csv
from keras.models import load_model
import joblib
from joblib import load
import requests
import json
import statsapi
import datetime
from creating_data import Baseball_player_data



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
    



def main():
    
    model, strikeout_scaler, input_scalers = load_model_and_scaler()

    # rand_game_s = statsapi.game()

    # Get names of pitchers
    # Get the data for the pitchers
    # Get names of batters going up against the pitchers
    # Get the data for the batters
    # Process all the data
    # Pass proccessed data to the model


    new_player_data = Baseball_player_data()  # Create an instance of the baseball_player_data class

    # Get today's date
    today = datetime.datetime.now()
    # Format the date as MM/DD/YYYY
    formatted_date = today.strftime("%m/%d/%Y")

    start_month_and_day = str(formatted_date[0:6])  # Get the month and day from the formatted date
    end_month_and_day = str(formatted_date[0:6])
    start_year = 2025
    end_year = 2025

    print(f"start_month_and_day: {start_month_and_day}")
    

    total_stats = new_player_data.get_names_and_strikeouts(start_month_and_day, end_month_and_day)  # Gets names and strikouts from pitchers, and names from batters
    total_stats = new_player_data.add_adv_pitcher_stats(total_stats)  # Adds advanced stats to the pitcher data
    total_stats = new_player_data.add_adv_batter_stats(total_stats)  # Adds advanced stats to the batter data
    total_stats = new_player_data.convert_to_float(total_stats)  # Converts the stats to float
    total_stats = new_player_data.calculate_avg_batter_stats(total_stats)  # Calculates the average batter stats for each pitcher

    
    # maybe write new write_to_csv function for the new player data?
    # new_player_data.write_to_csv(total_stats)  # Writes the total stats to a csv file



    # data = fetch_lineup_data()
 

    
    

if __name__ == "__main__":
    main()
