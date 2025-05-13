import random
import time
import csv
import json
import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import random
from random import randint
from sklearn.preprocessing import MinMaxScaler
from joblib import dump
import pickle
import joblib
import ast



def import_data():
    file_path = f"created_data/created_total_stats.csv"


    total_stats = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        reader.__next__()  # Skip the header row
        for row in reader:
            new_row = [row[0], float(row[1]), int(row[2]), ast.literal_eval(row[3]), ast.literal_eval(row[4])]
            total_stats.append(new_row)
    
    return total_stats



def process_strikeouts(total_stats):

    # Process strikeouts
    strikeout_scaler = MinMaxScaler(feature_range=(0,1))

    all_strikeouts = []
    for pitcher in total_stats:
        pitcher_strikeouts = pitcher[1]
        all_strikeouts.append(pitcher_strikeouts)
    
    numpy_strikeouts = np.array(all_strikeouts).reshape(-1, 1)  # Converts all numbers in training set to numpy.
    processed_strikeouts = strikeout_scaler.fit_transform(numpy_strikeouts)  # Fit the scaler to the data and transform it.

    return processed_strikeouts, strikeout_scaler


def process_pitcher_stats(total_stats):

    # Process pitcher stats

    all_processed_pitcher_stats = []

    all_pitcher_scalers = []

    for i in range(len(total_stats[0][3])): # Use the length of the first pitcher's stats for the loop

        single_stat_scaler = MinMaxScaler(feature_range=(0,1))

        all_single_stats = [] # holds all the stats for a stat type for every pitcher

        for pitcher in total_stats:

            pitcher_stats = pitcher[3] 

            stat = pitcher_stats[i]

            all_single_stats.append(stat)

        
        numpy_single_stats = np.array(all_single_stats).reshape(-1, 1)  # Converts all numbers in training set to numpy.
        processed_single_stats = single_stat_scaler.fit_transform(numpy_single_stats)  # Fit the scaler to the data and transform it.

        all_processed_pitcher_stats.append(processed_single_stats)  # Append the processed stats to the list

        all_pitcher_scalers.append(single_stat_scaler)  # Append the scaler to the list
    
    return all_processed_pitcher_stats, all_pitcher_scalers


def process_batter_stats(total_stats):

    # Process batter stats

    all_processed_batter_stats = []

    all_batter_scalers = []


    print(f"total_stats[4]: {total_stats[4]}")
    

    for i in range(len(total_stats[0][4])): # Use the length of the first pitcher's stats for the loop

        single_stat_scaler = MinMaxScaler(feature_range=(0,1))

        all_single_stats = [] # holds all the stats for a stat type for every pitcher

        for pitcher in total_stats:

            batter_stats = pitcher[4] 

            stat = batter_stats[i]

            all_single_stats.append(stat)

        
        numpy_single_stats = np.array(all_single_stats).reshape(-1, 1)  # Converts all numbers in training set to numpy.
        processed_single_stats = single_stat_scaler.fit_transform(numpy_single_stats)  # Fit the scaler to the data and transform it.

        all_processed_batter_stats.append(processed_single_stats)  # Append the processed stats to the list

        all_batter_scalers.append(single_stat_scaler)  # Append the scaler to the list
    
    print(f"all_processed_batter_stats: {len(all_processed_batter_stats)}")
    
    return all_processed_batter_stats, all_batter_scalers



def main():
    total_stats = import_data()

    processed_strikeouts, strikeout_scaler = process_strikeouts(total_stats)
    # Target
    y = processed_strikeouts

    # Features
    processed_pitcher_stats, all_pitcher_scalers = process_pitcher_stats(total_stats)
    processed_batter_stats, all_batter_scalers = process_batter_stats(total_stats)

    input_scalers = all_pitcher_scalers + all_batter_scalers
    
    print(f"processed_pitcher_stats: {len(processed_pitcher_stats)}")
    print(f"processed_batter_stats: {len(processed_batter_stats)}")
    print(f"processed_strikeouts: {len(processed_strikeouts)}")

    # print(f"processed_pitcher_stats viewed: {processed_pitcher_stats}")


    X = np.column_stack(processed_pitcher_stats + processed_batter_stats)
    



    '''# Convert list of 1-column arrays to a single array (num_samples, total_features)
    processed_pitcher_stats_matrix = np.hstack(processed_pitcher_stats)
    processed_batter_stats_matrix = np.hstack(processed_batter_stats)

    # Combine both into the final feature matrix
    X = np.hstack([processed_pitcher_stats_matrix, processed_batter_stats_matrix])'''


    print("Feature matrix X shape:", X.shape)
    print("Target vector y shape:", y.shape)


    joblib.dump(X, "processed_data/X.joblib")
    joblib.dump(y, "processed_data/y.joblib")

    dump(strikeout_scaler, 'model_and_scalers/strikeout_scaler.pkl')

    joblib.dump(input_scalers, 'model_and_scalers/input_scalers.pkl')




    return


    

if __name__ == "__main__":
    main()