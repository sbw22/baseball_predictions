import os

# Use legacy tf.keras behavior to improve compatibility when loading older/newer serialized models.
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")

import numpy as np
import csv
import joblib
from joblib import load
import requests
import json
import statsapi
import datetime
import keras
from creating_data import Baseball_player_data
from process_data import Process_player_data
from sklearn.preprocessing import MinMaxScaler
from keras.losses import MeanSquaredError, Huber
from keras.callbacks import EarlyStopping, ModelCheckpoint
from xgboost import XGBRegressor


def _infer_input_dim(input_scalers):
    if isinstance(input_scalers, dict):
        return len(input_scalers)
    if isinstance(input_scalers, (list, tuple)):
        return len(input_scalers)
    return 71

# This function builds the inference model architecture. It is used when loading the model weights if the full model cannot be loaded due to a batch shape error. The architecture is based on the one used during training, but it does not include the input layer with a specified batch shape, which allows it to be more flexible when loading weights.
def _build_inference_model(input_dim):
    return keras.Sequential([
        keras.layers.Input(shape=(input_dim,)),
        keras.layers.Dense(64, activation='silu'),
        keras.layers.LayerNormalization(),
        keras.layers.Dense(128, activation='silu'),
        keras.layers.LayerNormalization(),
        keras.layers.Dense(256, activation='silu'),
        keras.layers.LayerNormalization(),
        keras.layers.Dropout(0.1),
        keras.layers.Dense(512, activation='silu'),
        keras.layers.LayerNormalization(),
        keras.layers.Dropout(0.1),
        keras.layers.Dense(256, activation='silu'),
        keras.layers.LayerNormalization(),
        keras.layers.Dense(128, activation='silu'),
        keras.layers.LayerNormalization(),
        keras.layers.Dense(32, activation='silu'),
        keras.layers.LayerNormalization(),
        keras.layers.Dense(1)
    ])



def load_model_and_scaler():

    model_path = 'model_and_scalers/trained_strikeout_model.keras'
    weights_path = 'model_and_scalers/trained_strikeout_model_weights.weights.h5'

    strikeout_scaler = load('model_and_scalers/strikeout_scaler.pkl')
    input_scalers = joblib.load('model_and_scalers/input_scalers.pkl')
    all_pitcher_scalers = joblib.load('model_and_scalers/all_pitcher_scalers.pkl')
    all_batter_scalers = joblib.load('model_and_scalers/all_batter_scalers.pkl')

    try:
        model = keras.models.load_model(model_path, compile=False)
    except Exception as exc:
        if 'batch_shape' not in str(exc):
            raise

        input_dim = _infer_input_dim(input_scalers)
        model = _build_inference_model(input_dim)
        model.load_weights(weights_path)

    return model, strikeout_scaler, input_scalers, all_pitcher_scalers, all_batter_scalers




def get_future_stats():
    new_player_data = Baseball_player_data()  # Create an instance of the baseball_player_data class

    # Get today's date
    today = datetime.datetime.now()
    # Format the date as MM/DD/YYYY
    formatted_date = today.strftime("%m/%d/%Y")

    start_month_and_day = str(formatted_date[0:6])  # Get the month and day from the formatted date
    end_month_and_day = str(formatted_date[0:6])
    # start_month_and_day = "06/04/"
    # end_month_and_day = "06/04/"
    start_year = 2026
    end_year = 2026

    boilerplate_month_and_day = "05/02/"
    boilerplate_year = 2022

    print(f"start_month_and_day: {start_month_and_day}")

    boilerplate_stats = new_player_data.get_names_and_strikeouts(boilerplate_month_and_day, boilerplate_month_and_day, boilerplate_year, boilerplate_year)  # Gets stats from one game not in 2025. I am doing this because I think that if I have at least one game from 2024, the amount of inputs into the model will be correct
    boilerplate_stats = [boilerplate_stats[0]]  # Adds an extra dimension to the boilerplate stats so that it can be added to the future stats

    print(f"boilerplate_stats: {boilerplate_stats}")
    print(f"boilerplate_stats length: {len(boilerplate_stats)}")
    
    boilerplate_stats = new_player_data.add_adv_pitcher_stats(boilerplate_stats)  # Adds advanced stats to the pitcher data
    boilerplate_stats = new_player_data.add_adv_batter_stats(boilerplate_stats)  # Adds advanced stats to the batter data
    boilerplate_stats = new_player_data.convert_to_float(boilerplate_stats)  # Converts the stats to float
    boilerplate_stats = new_player_data.calculate_avg_batter_stats(boilerplate_stats)
    


    future_stats = new_player_data.get_names_and_strikeouts(start_month_and_day, end_month_and_day, start_year, end_year)  # Gets names and strikouts from pitchers, and names from batters
    for item in future_stats:
        print(f"future_stats item: {item}")
    try:
        print(f"future_stats[[0]: {future_stats[0]}")
    except:
        print(f"Error: future_stats = {future_stats}")
    
    game_visual(start_month_and_day, end_month_and_day, start_year, end_year)  # Gets visual of boxscores

    future_stats = new_player_data.add_adv_pitcher_stats(future_stats)  # Adds advanced stats to the pitcher data
    print(f"future_stats after adding adv pitcher stats: {future_stats}")
    future_stats = new_player_data.add_adv_batter_stats(future_stats)  # Adds advanced stats to the batter data
    future_stats = new_player_data.convert_to_float(future_stats)  # Converts the stats to float
    future_stats = new_player_data.calculate_avg_batter_stats(future_stats)  # Calculates the average batter stats for each pitcher

    future_stats = boilerplate_stats + future_stats  # Adds the boilerplate stats to the future stats

    print(f"future_stats after adding all stats: {future_stats}")
    # fdgs
    
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


def predict_strikeouts(model, X, strikeout_scaler, future_stats, output_filename):
    # Evaluate the model
    if isinstance(model, XGBRegressor):
        predictions = np.asarray(model.predict(X)).reshape(-1, 1)
    else:
        predictions = np.asarray(model.predict(X, batch_size=1, verbose=0)).reshape(-1, 1)
    # loss, accuracy = model.evaluate(X, y)

    scaled_up_guesses = strikeout_scaler.inverse_transform(predictions)
    rounded_guesses = np.round(scaled_up_guesses)

    results = []
    for i in range(1, len(rounded_guesses)):  #  Skip the first element because it is the boilerplate stats
        pitcher_name = future_stats[i][0]
        team = future_stats[i][5] if len(future_stats[i]) > 5 else ""
        guess = round(float(rounded_guesses[i].item()), 2)
        print(f"\n{pitcher_name}'s predicted strikeouts: {guess}\n")
        results.append({"name": pitcher_name, "k": guess, "team": team})
    
    # Save to predictions.json in the same format server.py used
    output = {
        "status": "ok",
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "predictions": results,
    }
    with open(output_filename, "w") as f:
        json.dump(output, f)
    if output_filename == "regression_predictions.json":
        with open("predictions.json", "w") as f:
            json.dump(output, f)
    print(f"\nSaved {len(results)} predictions to {output_filename}")

    return predictions


def main():
    
    model, strikeout_scaler, input_scalers, all_pitcher_scalers, all_batter_scalers = load_model_and_scaler()
    xgboost_model = joblib.load('model_and_scalers/trained_strikeout_model_xgboost.joblib')

    
    # Get names of pitchers
    # Get the data for the pitchers
    # Get names of batters going up against the pitchers
    # Get the data for the batters
    # Process all the data
    # Pass proccessed data to the model


    future_stats = get_future_stats()  # Gets the future stats from the baseball_player_data class
    try:
        print(f"future_stats 'strikeouts': {future_stats[1]}")
    except IndexError:
        print("Error: No pitchers stats are available at the moment.")

    process_player_data = Process_player_data()

    processed_pitcher_stats, all_pitcher_scalers = process_player_data.process_pitcher_stats(future_stats)
    processed_batter_stats, all_batter_scalers = process_player_data.process_batter_stats(future_stats)

    print(f"processed_pitcher_stats: {len(processed_pitcher_stats)}")
    print(f"processed_batter_stats: {len(processed_batter_stats)}")

    X = np.column_stack(processed_pitcher_stats + processed_batter_stats)

    # print(f"X shape: {X.shape}")
    # print(f"future_stats shape: {len(future_stats)}")

    predict_strikeouts(model, X, strikeout_scaler, future_stats, "regression_predictions.json")  # Predicts the strikeouts for the pitchers
    predict_strikeouts(xgboost_model, X, strikeout_scaler, future_stats, "xgboost_predictions.json")



'''
git add .
git commit -m "daily update to stats and predictions"
git push origin main
'''

'''
crontab -l = view current cron table
crontab -r = remove current cron table
crontab -e = edit current cron table
'''

    

if __name__ == "__main__":
    main()
