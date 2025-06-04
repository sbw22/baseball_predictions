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

    early_stop = EarlyStopping(monitor='val_loss', patience=200, restore_best_weights=True)
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

    avg_error = 0.0
    match_counter = 0
    within_one = 0
    within_two = 0
    within_three = 0
    within_four = 0
    within_five = 0
    within_six = 0

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


        print(f"Predicted strikeouts: {guess}")
        print(f"Actual strikeouts: {actual}\n")
    
    avg_error /= len(rounded_guesses)

    print(f"Average error: {avg_error:.2f}\n")

    print(f"Perfect guesses: {match_counter} out of {len(rounded_guesses)} -- {match_counter / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within one strikeout: {within_one} out of {len(rounded_guesses)} -- {within_one / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within two strikeouts: {within_two} out of {len(rounded_guesses)} -- {within_two / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within three strikeouts: {within_three} out of {len(rounded_guesses)} -- {within_three / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within four strikeouts: {within_four} out of {len(rounded_guesses)} -- {within_four / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within five strikeouts: {within_five} out of {len(rounded_guesses)} -- {within_five / len(rounded_guesses) * 100:.2f}%\n")
    print(f"Within six strikeouts: {within_six} out of {len(rounded_guesses)} -- {within_six / len(rounded_guesses) * 100:.2f}%\n")

    return predictions
    



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