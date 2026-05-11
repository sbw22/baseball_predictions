import numpy as np
import os
import random
import tensorflow as tf
from random import randint
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

import keras
from keras.models import Sequential, Model
from keras.layers import Activation
from keras.optimizers import Adam
from keras.losses import Huber, LogCosh
from keras.callbacks import EarlyStopping
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from keras import backend as K
from tensorflow.keras.layers import Flatten, Dropout, BatchNormalization, Concatenate, Input
from keras.metrics import categorical_crossentropy
from tensorflow.keras.layers import *
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
from keras.callbacks import ModelCheckpoint
from xgboost import XGBRegressor
from results_metrics import ResultsMetrics
# import TweedieLoss as Tweedie


# ---- Seed control ---- # This adds reproducability to the output
def set_seeds(seed=42):
    np.random.seed(seed)        # NumPy
    random.seed(seed)           # Python built-in
    tf.random.set_seed(seed)    # TensorFlow/Keras
    os.environ["PYTHONHASHSEED"] = str(seed)

set_seeds()


def create_model(X):
    # Create a simple feedforward neural network

    # IF YOU EDIT THIS ARCHITECTURE, MAKE SURE TO UPDATE THE _build_inference_model FUNCTION IN future_game_predictor.py 
    # TO MATCH THE NEW ARCHITECTURE (EXCEPT FOR THE INPUT LAYER, WHICH SHOULD NOT HAVE A BATCH SHAPE SPECIFIED)
    model = keras.Sequential([
        Input(shape=(X.shape[1],)),

        Dense(64, activation='silu'),
        LayerNormalization(),
        # Dropout(0.1),

        Dense(128, activation='silu'),
        LayerNormalization(),
        # Dropout(0.1),

        Dense(256, activation='silu'),
        LayerNormalization(),
        Dropout(0.1),

        Dense(512, activation='silu'),
        LayerNormalization(),
        Dropout(0.1),

        Dense(256, activation='silu'),
        LayerNormalization(),
        # Dropout(0.1),

        Dense(128, activation='silu'),
        LayerNormalization(),
        # Dropout(0.1),

        Dense(32, activation='silu'),
        LayerNormalization(),
        # Dropout(0.1),

        Dense(1)
    ])

    # Compile the model
    model.compile(
        loss='mse',
        optimizer=tf.keras.optimizers.AdamW(),
        metrics=['mae', tf.keras.metrics.RootMeanSquaredError(name='rmse')]
    )
    # model.compile(loss='mse', optimizer='AdamW', metrics=['mae', tf.keras.metrics.RootMeanSquaredError(name='rmse')])
    # List of losses to try: Huber, MAE, MSE, LogCosh, QuantileLoss (need to specify quantiles), Poisson, Tweedie, CategoricalCrossentropy (for classification), BinaryCrossentropy (for binary classification)
    # loss=Huber(delta=1.0)

    return model


def create_xgboost_model():
    return XGBRegressor(
        objective='reg:squarederror',
        n_estimators=500,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )

def train_model(X, y, strikeout_scaler, model):

    early_stop = EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True)
    checkpoint = ModelCheckpoint('model_and_scalers/best_model.h5', save_best_only=True)
    y_unscaled = strikeout_scaler.inverse_transform(y.reshape(-1, 1)).ravel()
    z = (y_unscaled - y_unscaled.mean()) / (y_unscaled.std() + 1e-8)
    sample_weight = 1.0 + 0.5 * np.maximum(0.0, z - 1.0)

    # Train the model
    model.fit(X, y, epochs=1000, validation_split=0.2, batch_size=64, callbacks=[early_stop, checkpoint], sample_weight=sample_weight)

    return model


def train_xgboost_model(X, y, strikeout_scaler, model):
    y_unscaled = strikeout_scaler.inverse_transform(y.reshape(-1, 1)).ravel()
    z = (y_unscaled - y_unscaled.mean()) / (y_unscaled.std() + 1e-8)
    sample_weight = 1.0 + 0.5 * np.maximum(0.0, z - 1.0)
    model.fit(X, y, sample_weight=sample_weight)
    return model

def run_model(model, X, y, strikeout_scaler, results_metrics):
    # Evaluate the model
    predictions = model.predict(X, batch_size=1, verbose=0)
    # loss, accuracy = model.evaluate(X, y)

    scaled_up_guesses = strikeout_scaler.inverse_transform(predictions)
    rounded_guesses = np.round(scaled_up_guesses)
    scaled_up_actual_strikeouts = strikeout_scaler.inverse_transform(y.reshape(-1, 1))

    return results_metrics.print_and_save_results(rounded_guesses, scaled_up_guesses, scaled_up_actual_strikeouts)


def run_xgboost_model(model, X, y, strikeout_scaler, results_metrics):
    predictions = model.predict(X).reshape(-1, 1)
    scaled_up_guesses = strikeout_scaler.inverse_transform(predictions)
    rounded_guesses = np.round(scaled_up_guesses)
    scaled_up_actual_strikeouts = strikeout_scaler.inverse_transform(y.reshape(-1, 1))

    return results_metrics.print_and_save_results(rounded_guesses, scaled_up_guesses, scaled_up_actual_strikeouts)


def main():
    
    results_metrics = ResultsMetrics()

    X = joblib.load("processed_data/X.joblib")
    y = joblib.load("processed_data/y.joblib")

    print(f"x length: {len(X)}")

    print(f"X: {X.shape}")

    strikeout_scaler = load('model_and_scalers/strikeout_scaler.pkl')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"len of y_train: {len(y_train)}")
    print(f"len of y_test: {len(y_test)}")

    

    regression_model = create_model(X)
    xgboost_model = create_xgboost_model()

    print(f"Training XGBoost model...")
    train_xgboost_model(X_train, y_train, strikeout_scaler, xgboost_model)
    xgboost_within_percents_list = run_xgboost_model(xgboost_model, X_test, y_test, strikeout_scaler, results_metrics)

    print(f"Training Keras model...")
    train_model(X_train, y_train, strikeout_scaler, regression_model)
    regression_within_percents_list = run_model(regression_model, X_test, y_test, strikeout_scaler, results_metrics)


    # save/return the performance metrics from this model run so we can display them on the frontend
    # save regression metrics
    with open('model_and_scalers/regression_performance_metrics.json', 'w') as f:
        json.dump({
            'perfect_guess': f"{regression_within_percents_list[0]:.2f} %",
            'within_1': f"{regression_within_percents_list[1]:.2f} %",
            'within_2': f"{regression_within_percents_list[2]:.2f} %",
            'within_3': f"{regression_within_percents_list[3]:.2f} %",
            'within_4': f"{regression_within_percents_list[4]:.2f} %",
            'within_5': f"{regression_within_percents_list[5]:.2f} %",
            'within_6': f"{regression_within_percents_list[6]:.2f} %"
        }, f)  # <-- add f here
    # save xgboost metrics
    with open('model_and_scalers/xgboost_performance_metrics.json', 'w') as f:
        json.dump({
            'perfect_guess': f"{xgboost_within_percents_list[0]:.2f} %",
            'within_1': f"{xgboost_within_percents_list[1]:.2f} %",
            'within_2': f"{xgboost_within_percents_list[2]:.2f} %",
            'within_3': f"{xgboost_within_percents_list[3]:.2f} %",
            'within_4': f"{xgboost_within_percents_list[4]:.2f} %",
            'within_5': f"{xgboost_within_percents_list[5]:.2f} %",
            'within_6': f"{xgboost_within_percents_list[6]:.2f} %"
        }, f)  # <-- add f here


    # Save both models (the Keras regression model and the XGBoost model), so we can load them in the future for inference on new data. We save both the entire Keras model and just the weights, so that we have the option to load just the weights into a new model architecture in the future if we want to experiment with different architectures without having to retrain from scratch each time.
    
    joblib.dump(xgboost_model, 'model_and_scalers/trained_strikeout_model_xgboost.joblib')
    regression_model.save('model_and_scalers/trained_strikeout_model.keras', include_optimizer=False)
    regression_model.save_weights('model_and_scalers/trained_strikeout_model_weights.weights.h5')

    # print(X.shape, y.shape)



if __name__ == "__main__":
    main()