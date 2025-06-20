import numpy as np
import random
from random import randint
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import keras
from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Activation
from tensorflow.keras.layers import Flatten, Dropout, BatchNormalization, Concatenate
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from tensorflow.keras.layers import *
from keras.models import Model
from keras.applications import imagenet_utils
import matplotlib.pyplot as plt 
from sklearn.metrics import confusion_matrix
import itertools
from joblib import load
import pickle
import csv
import json
import joblib
import math
from keras.losses import Huber
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint



def create_model(X):
    # Create a simple feedforward neural network


    model = Sequential([
        Input(shape=(X.shape[1],)),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.1),

        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.1),

        Dense(32, activation='relu'),
        BatchNormalization(),
        Dropout(0.1),

        Dense(1)
    ])

    # Compile the model
    model.compile(loss=Huber(delta=1.0), optimizer='adam', metrics=['mae'])

    return model

def train_model(X, y, strikeout_scaler, model):

    early_stop = EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True)
    checkpoint = ModelCheckpoint('model_and_scalers/best_model.h5', save_best_only=True)

    # Train the model
    model.fit(X, y, epochs=1000, validation_split=0.2, batch_size=64, callbacks=[early_stop, checkpoint])

    return model

def run_model(model, X, y, strikeout_scaler):
    # Evaluate the model
    predictions = model.predict(X, batch_size=1, verbose=0)
    # loss, accuracy = model.evaluate(X, y)

    scaled_up_guesses = strikeout_scaler.inverse_transform(predictions)
    rounded_guesses = np.round(scaled_up_guesses)
    scaled_up_actual_strikeouts = strikeout_scaler.inverse_transform(y.reshape(-1, 1))

    print_and_save_results(rounded_guesses, scaled_up_guesses, scaled_up_actual_strikeouts)


def print_and_save_results(rounded_guesses, scaled_up_guesses, scaled_up_actual_strikeouts):

    avg_error = 0.0
    match_counter = 0
    within_one = 0
    within_two = 0
    within_three = 0
    within_four = 0
    within_five = 0
    within_six = 0

    total_num_of_so = [0,0,0,0,0,0,0,0,0,0]

    correct_num_of_so = [0,0,0,0,0,0,0,0,0,0]
    within_1_num_of_so = [0,0,0,0,0,0,0,0,0,0]
    within_2_num_of_so = [0,0,0,0,0,0,0,0,0,0]
    within_3_num_of_so = [0,0,0,0,0,0,0,0,0,0]
    within_4_num_of_so = [0,0,0,0,0,0,0,0,0,0]
    within_5_num_of_so = [0,0,0,0,0,0,0,0,0,0]
    within_6_num_of_so = [0,0,0,0,0,0,0,0,0,0]

    master_num_of_so = [correct_num_of_so, within_1_num_of_so, within_2_num_of_so, within_3_num_of_so, within_4_num_of_so, within_5_num_of_so, within_6_num_of_so]

    '''correct_on_1 = 0
    correct_on_2 = 0
    correct_on_3 = 0
    correct_on_4 = 0
    correct_on_5 = 0
    correct_on_6 = 0
    correct_on_7 = 0
    correct_on_8 = 0
    correct_on_9 = 0'''

    for i in range(len(rounded_guesses)):
        guess = round(rounded_guesses[i].item(), 2)
        actual = round(scaled_up_actual_strikeouts[i].item(), 2)

        avg_error += abs(guess - actual)

        match_counter += 1 if guess == actual else 0
        within_one += 1 if abs(guess - actual) <= 1 else 0
        within_two += 1 if abs(guess - actual) <= 2 else 0
        within_three += 1 if abs(guess - actual) <= 3 else 0
        within_four += 1 if abs(guess - actual) <= 4 else 0
        within_five += 1 if abs(guess - actual) <= 5 else 0
        within_six += 1 if abs(guess - actual) <= 6 else 0

        total_num_of_so[int(actual)] += 1

        correct_num_of_so[int(actual)] += 1 if guess == actual else 0
        within_1_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 1 else 0
        within_2_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 2 else 0
        within_3_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 3 else 0
        within_4_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 4 else 0
        within_5_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 5 else 0
        within_6_num_of_so[int(actual)] += 1 if abs(guess - actual) <= 6 else 0


        print(f"Predicted strikeouts: {guess}")
        print(f"Actual strikeouts: {actual}\n")

    # Calculate percent correct of guesses in each category
    
    for num_of_so in master_num_of_so:
        for i in range(len(num_of_so)):
            new_percent = 0.0
            if total_num_of_so[i] > 0:
                new_percent = round(num_of_so[i] / total_num_of_so[i] * 100, 2)

            else:
                new_percent = 0.0
            num_of_so[i] = [num_of_so[i], new_percent]



    avg_error /= len(rounded_guesses)

    print(f"Average error: {avg_error:.2f}\n")

    print(f"Perfect guesses: {match_counter} out of {len(rounded_guesses)} -- {match_counter / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within one strikeout: {within_one} out of {len(rounded_guesses)} -- {within_one / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within two strikeouts: {within_two} out of {len(rounded_guesses)} -- {within_two / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within three strikeouts: {within_three} out of {len(rounded_guesses)} -- {within_three / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within four strikeouts: {within_four} out of {len(rounded_guesses)} -- {within_four / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within five strikeouts: {within_five} out of {len(rounded_guesses)} -- {within_five / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within six strikeouts: {within_six} out of {len(rounded_guesses)} -- {within_six / len(rounded_guesses) * 100:.2f}%\n\n")

    
    
    for i in range(10):
        try:
            print(f"Correct guesses for {i} strikeouts: {correct_num_of_so[i][0]} out of {total_num_of_so[i]} -- {correct_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")

        except ZeroDivisionError:
            print(f"Correct guesses for {i} strikeouts: {correct_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")

        try:
            print(f"Within 1 strikeouts for {i} strikeouts: {within_1_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_1_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
        except ZeroDivisionError:
            print(f"Within 1 strikeouts for {i} strikeouts: {within_1_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")

        try:
            print(f"Within 2 strikeouts for {i} strikeouts: {within_2_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_2_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
        except ZeroDivisionError:
            print(f"Within 2 strikeouts for {i} strikeouts: {within_2_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")

        try:
            print(f"Within 3 strikeouts for {i} strikeouts: {within_3_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_3_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
        except ZeroDivisionError:
            print(f"Within 3 strikeouts for {i} strikeouts: {within_3_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")
        try:
            print(f"Within 4 strikeouts for {i} strikeouts: {within_4_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_4_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
        except ZeroDivisionError:
            print(f"Within 4 strikeouts for {i} strikeouts: {within_4_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")
        try:
            print(f"Within 5 strikeouts for {i} strikeouts: {within_5_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_5_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
        except ZeroDivisionError:
            print(f"Within 5 strikeouts for {i} strikeouts: {within_5_num_of_so[i][0]} out of {total_num_of_so[i]} -- 0.00%\n")
        try:
            print(f"Within 6 strikeouts for {i} strikeouts: {within_6_num_of_so[i][0]} out of {total_num_of_so[i]} -- {within_6_num_of_so[i][0] / total_num_of_so[i] * 100:.2f}%\n")
        except ZeroDivisionError:
            print(f"Within 6 strikeouts for {i} strikeouts: {within_6_num_of_so[i]} out of {total_num_of_so[i]} -- 0.00%\n")


    # import above data to a csv file
    with open('prediction_stats/strikeout_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['actual_strikeouts', 'total_guesses', 'correct_guesses', 'within_1', 'within_2', 'within_3', 'within_4', 'within_5', 'within_6']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(10):
            try:
                writer.writerow({
                    'actual_strikeouts': i,
                    'total_guesses': total_num_of_so[i],
                    'correct_guesses': correct_num_of_so[i][0],
                    'within_1': within_1_num_of_so[i][0],
                    'within_2': within_2_num_of_so[i][0],
                    'within_3': within_3_num_of_so[i][0],
                    'within_4': within_4_num_of_so[i][0],
                    'within_5': within_5_num_of_so[i][0],
                    'within_6': within_6_num_of_so[i][0]
                })
            except ZeroDivisionError:
                writer.writerow({
                    'actual_strikeouts': i,
                    'total_guesses': 0,
                    'correct_guesses': 0,
                    'within_1': 0,
                    'within_2': 0,
                    'within_3': 0,
                    'within_4': 0,
                    'within_5': 0,
                    'within_6': 0
                })
        
        # Write another row with the fieldnames
        writer.writerow({})

        writer.writerow({
            'actual_strikeouts': 'actual_strikeouts - percentages',
            'total_guesses': 'total_guesses',
            'correct_guesses': 'correct_guesses',
            'within_1': 'within_1',
            'within_2': 'within_2',
            'within_3': 'within_3',
            'within_4': 'within_4',
            'within_5': 'within_5',
            'within_6': 'within_6'
        })

        for i in range(10):
            try:
                writer.writerow({
                    'actual_strikeouts': i,
                    'total_guesses': total_num_of_so[i],
                    'correct_guesses': f'{correct_num_of_so[i][1]} + %',
                    'within_1': f'{within_1_num_of_so[i][1]} + %',
                    'within_2': f'{within_2_num_of_so[i][1]} + %',
                    'within_3': f'{within_3_num_of_so[i][1]} + %',
                    'within_4': f'{within_4_num_of_so[i][1]} + %',
                    'within_5': f'{within_5_num_of_so[i][1]} + %',
                    'within_6': f'{within_6_num_of_so[i][1]} + %'
                })
            except ZeroDivisionError:
                writer.writerow({
                    'actual_strikeouts': i,
                    'total_guesses': '0.0 %',
                    'correct_guesses': '0.0 %',
                    'within_1': '0.0 %',
                    'within_2': '0.0 %',
                    'within_3': '0.0 %',
                    'within_4': '0.0 %',
                    'within_5': '0.0 %',
                    'within_6': '0.0 %'
                })



    '''# Print the confusion matrix
    cm = confusion_matrix(scaled_up_actual_strikeouts, rounded_guesses)
    plt.figure(figsize=(10, 7))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(10)
    plt.xticks(tick_marks, range(10))
    plt.yticks(tick_marks, range(10))
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig('prediction_stats/confusion_matrix.png')
    plt.show()'''


    # --- Heatmap for counts ---
    counts_matrix = np.array([
        [correct_num_of_so[i][0], within_1_num_of_so[i][0], within_2_num_of_so[i][0], within_3_num_of_so[i][0],
         within_4_num_of_so[i][0], within_5_num_of_so[i][0], within_6_num_of_so[i][0]]
        for i in range(10)
    ])
    plt.figure(figsize=(10, 7))
    plt.imshow(counts_matrix, cmap='coolwarm', aspect='auto', vmin=0, vmax=np.max(counts_matrix))
    plt.colorbar(label='Count')
    plt.xticks(range(7), ['Exact', 'Within 1', 'Within 2', 'Within 3', 'Within 4', 'Within 5', 'Within 6'])
    plt.yticks(range(10), [str(i) for i in range(10)])
    for i in range(counts_matrix.shape[0]):
        for j in range(counts_matrix.shape[1]):
            plt.text(j, i, counts_matrix[i, j], ha='center', va='center', color='black', fontsize=10, alpha=0.8)
    plt.title('Strikeout Prediction Counts Heatmap')
    plt.xlabel('Prediction Accuracy')
    plt.ylabel('Actual Strikeouts')
    plt.tight_layout()
    plt.savefig('prediction_stats/strikeout_counts_heatmap.png', dpi=200)
    plt.close()

    # --- Heatmap for percentages ---
    percent_matrix = np.array([
        [correct_num_of_so[i][1], within_1_num_of_so[i][1], within_2_num_of_so[i][1], within_3_num_of_so[i][1],
         within_4_num_of_so[i][1], within_5_num_of_so[i][1], within_6_num_of_so[i][1]]
        for i in range(10)
    ])
    plt.figure(figsize=(10, 7))
    plt.imshow(percent_matrix, cmap='coolwarm', aspect='auto', vmin=0, vmax=100)
    plt.colorbar(label='Percent')
    plt.xticks(range(7), ['Exact', 'Within 1', 'Within 2', 'Within 3', 'Within 4', 'Within 5', 'Within 6'])
    plt.yticks(range(10), [str(i) for i in range(10)])
    for i in range(percent_matrix.shape[0]):
        for j in range(percent_matrix.shape[1]):
            plt.text(j, i, f"{percent_matrix[i, j]:.1f}%", ha='center', va='center', color='black', fontsize=10, alpha=0.8)
    plt.title('Strikeout Prediction Percentages Heatmap')
    plt.xlabel('Prediction Accuracy')
    plt.ylabel('Actual Strikeouts')
    plt.tight_layout()
    plt.savefig('prediction_stats/strikeout_percentages_heatmap.png', dpi=200)
    plt.close()
    

    return
    



def main():
    

    X = joblib.load("processed_data/X.joblib")
    y = joblib.load("processed_data/y.joblib")

    print(f"x length: {len(X)}")

    print(f"X: {X.shape}")

    strikeout_scaler = load('model_and_scalers/strikeout_scaler.pkl')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    model = create_model(X)

    train_model(X_train, y_train, strikeout_scaler, model)

    predictions = run_model(model, X_test, y_test, strikeout_scaler)



    # Save the model
    model.save('model_and_scalers/trained_strikeout_model.h5')  # Save the full model to a file


    # print(X.shape, y.shape)



if __name__ == "__main__":
    main()