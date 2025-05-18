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
from process_data import Process_player_data
from sklearn.preprocessing import MinMaxScaler



def load_model_and_scaler():

    model = load_model(f'model_and_scalers/trained_strikeout_model.h5')

    strikeout_scaler = load('model_and_scalers/strikeout_scaler.pkl')

    input_scalers = joblib.load('model_and_scalers/input_scalers.pkl')

    all_pitcher_scalers = joblib.load('model_and_scalers/all_pitcher_scalers.pkl')

    all_batter_scalers = joblib.load('model_and_scalers/all_batter_scalers.pkl')

    return model, strikeout_scaler, input_scalers, all_pitcher_scalers, all_batter_scalers




def get_future_stats():
    new_player_data = Baseball_player_data()  # Create an instance of the baseball_player_data class

    # Get today's date
    today = datetime.datetime.now()
    # Format the date as MM/DD/YYYY
    formatted_date = today.strftime("%m/%d/%Y")

    #start_month_and_day = str(formatted_date[0:6])  # Get the month and day from the formatted date
    #end_month_and_day = str(formatted_date[0:6])
    start_month_and_day = "05/18/"
    end_month_and_day = "05/18/"
    start_year = 2025
    end_year = 2025

    print(f"start_month_and_day: {start_month_and_day}")
    

    future_stats = new_player_data.get_names_and_strikeouts(start_month_and_day, end_month_and_day, start_year, end_year)  # Gets names and strikouts from pitchers, and names from batters
    
    game_visual(start_month_and_day, end_month_and_day, start_year, end_year)  # Gets visual of boxscores

    future_stats = new_player_data.add_adv_pitcher_stats(future_stats)  # Adds advanced stats to the pitcher data
    future_stats = new_player_data.add_adv_batter_stats(future_stats)  # Adds advanced stats to the batter data
    future_stats = new_player_data.convert_to_float(future_stats)  # Converts the stats to float
    future_stats = new_player_data.calculate_avg_batter_stats(future_stats)  # Calculates the average batter stats for each pitcher

    # print(f"future_stats after calculate_avg_batter_stats: {future_stats}")

    return future_stats




def game_visual(start_month_and_day, end_month_and_day, start_year, end_year):

        total_stats = []

        curr_year = 0

        for year in range(start_year, end_year+1): # end year is the last year to check, which is why we add 1 to the end_year

            games = statsapi.schedule(start_date=f'{start_month_and_day}{year}',end_date=f'{end_month_and_day}{year}')

            # Print the game IDs
            game_ids = []

            for i in range(len(games)):
                game_ids.append(games[i]['game_id'])

            for game_id in game_ids:
                new_year = year
                if new_year != curr_year:
                    curr_year = new_year
                    print(f"curr_year = {curr_year}")

                game = statsapi.boxscore(game_id, battingBox=True, battingInfo=True, fieldingInfo=True, pitchingBox=True, gameInfo=True, timecode=None)        
                
                game_array = game.split("\n")

                # Print the game array
                for i in range(len(game_array)):
                    print(f"line[{i}] = {game_array[i]}")
                print() # to get space between games




def predict_strikeouts(model, X, strikeout_scaler, future_stats):
    # Evaluate the model
    predictions = model.predict(X, batch_size=1, verbose=0)
    # loss, accuracy = model.evaluate(X, y)

    scaled_up_guesses = strikeout_scaler.inverse_transform(predictions)
    rounded_guesses = np.round(scaled_up_guesses)


    for i in range(len(rounded_guesses)):

        pitcher_name = future_stats[i][0]

        guess = round(rounded_guesses[i].item(), 2)

        print(f"{pitcher_name}'s predicted strikeouts: {guess}\n")


    return predictions



    



def main():
    
    model, strikeout_scaler, input_scalers, all_pitcher_scalers, all_batter_scalers = load_model_and_scaler()

    
    # Get names of pitchers
    # Get the data for the pitchers
    # Get names of batters going up against the pitchers
    # Get the data for the batters
    # Process all the data
    # Pass proccessed data to the model


    future_stats = get_future_stats()  # Gets the future stats from the baseball_player_data class

    process_player_data = Process_player_data()

    processed_pitcher_stats, all_pitcher_scalers = process_player_data.process_pitcher_stats(future_stats)
    processed_batter_stats, all_batter_scalers = process_player_data.process_batter_stats(future_stats)

    X = np.column_stack(processed_pitcher_stats + processed_batter_stats)




    

if __name__ == "__main__":
    main()
