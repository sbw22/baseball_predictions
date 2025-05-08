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

    return processed_strikeouts


def process_pitcher_stats(total_stats):

    # Process pitcher stats

    all_processed_pitcher_stats = []

    for i in range(len(total_stats[3][0])): # Use the length of the first pitcher's stats for the loop

        single_stat_scaler = MinMaxScaler(feature_range=(0,1))

        all_single_stats = [] # holds all the stats for a stat type for every pitcher

        for pitcher in total_stats:

            pitcher_stats = pitcher[3] 

            stat = pitcher_stats[i]

            all_single_stats.append(stat)

        
        numpy_single_stats = np.array(all_single_stats).reshape(-1, 1)  # Converts all numbers in training set to numpy.
        processed_single_stats = single_stat_scaler.fit_transform(numpy_single_stats)  # Fit the scaler to the data and transform it.

        all_processed_pitcher_stats.append(processed_single_stats)  # Append the processed stats to the list
    
    return all_processed_pitcher_stats


def process_batter_stats(total_stats):

    # Process batter stats

    all_processed_batter_stats = []

    for i in range(len(total_stats[4][0])): # Use the length of the first pitcher's stats for the loop

        single_stat_scaler = MinMaxScaler(feature_range=(0,1))

        all_single_stats = [] # holds all the stats for a stat type for every pitcher

        for pitcher in total_stats:

            batter_stats = pitcher[4] 

            stat = batter_stats[i]

            all_single_stats.append(stat)

        
        numpy_single_stats = np.array(all_single_stats).reshape(-1, 1)  # Converts all numbers in training set to numpy.
        processed_single_stats = single_stat_scaler.fit_transform(numpy_single_stats)  # Fit the scaler to the data and transform it.

        all_processed_batter_stats.append(processed_single_stats)  # Append the processed stats to the list
    
    return all_processed_batter_stats



def main():
    total_stats = import_data()

    processed_strikeouts = process_strikeouts(total_stats)
    # Target
    y = processed_strikeouts

    # Features
    processed_pitcher_stats = process_pitcher_stats(total_stats)
    processed_batter_stats = process_batter_stats(total_stats)

    # Combine all stats into a single feature matrix
    X = np.hstack(processed_pitcher_stats + processed_batter_stats)  # shape: (num_samples, total_features)

    print("Feature matrix X shape:", X.shape)
    print("Target vector y shape:", y.shape)

    print(f"at end")

    joblib.dump(X, "processed_data/X.joblib")
    joblib.dump(y, "processed_data/y.joblib")



    return


    

if __name__ == "__main__":
    main()