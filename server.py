from flask import Flask, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from flask_cors import CORS
import numpy as np
import joblib
import datetime
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

# ── Import your existing modules ──────────────────────────────────────────────
from creating_data import Baseball_player_data
from process_data import Process_player_data
from keras.models import load_model
import keras

app = Flask(__name__, static_folder=".")
CORS(app)  # Enable CORS for all routes


def load_model_and_scaler():
    # model = load_model("model_and_scalers/trained_strikeout_model.keras", compile=False)
    model = keras.models.load_model(
        "model_and_scalers/trained_strikeout_model.keras",
        compile=False,
        safe_mode=False   # allows loading older saved models
    )
    strikeout_scaler = joblib.load("model_and_scalers/strikeout_scaler.pkl")
    input_scalers = joblib.load("model_and_scalers/input_scalers.pkl")
    all_pitcher_scalers = joblib.load("model_and_scalers/all_pitcher_scalers.pkl")
    all_batter_scalers = joblib.load("model_and_scalers/all_batter_scalers.pkl")
    return model, strikeout_scaler, input_scalers, all_pitcher_scalers, all_batter_scalers


def get_future_stats():
    new_player_data = Baseball_player_data()

    today = datetime.datetime.now()
    formatted_date = today.strftime("%m/%d/%Y")
    start_month_and_day = str(formatted_date[0:6])
    end_month_and_day = str(formatted_date[0:6])
    start_year = 2026
    end_year = 2026

    boilerplate_month_and_day = "05/02/"
    boilerplate_year = 2022

    boilerplate_stats = new_player_data.get_names_and_strikeouts(
        boilerplate_month_and_day, boilerplate_month_and_day, boilerplate_year, boilerplate_year
    )
    boilerplate_stats = [boilerplate_stats[0]]
    boilerplate_stats = new_player_data.add_adv_pitcher_stats(boilerplate_stats)
    boilerplate_stats = new_player_data.add_adv_batter_stats(boilerplate_stats)
    boilerplate_stats = new_player_data.convert_to_float(boilerplate_stats)
    boilerplate_stats = new_player_data.calculate_avg_batter_stats(boilerplate_stats)

    future_stats = new_player_data.get_names_and_strikeouts(
        start_month_and_day, end_month_and_day, start_year, end_year
    )
    future_stats = new_player_data.add_adv_pitcher_stats(future_stats)
    future_stats = new_player_data.add_adv_batter_stats(future_stats)
    future_stats = new_player_data.convert_to_float(future_stats)
    future_stats = new_player_data.calculate_avg_batter_stats(future_stats)
    future_stats = boilerplate_stats + future_stats

    return future_stats


@app.route("/")
def index():
    return send_from_directory(".", "index.html") # Changed to index.html from strikeout_predictions.html for simplicity

@app.route("/mlb_teams_logo_svg/light/<path:filename>")
def serve_logo(filename):
    return send_from_directory("mlb_teams_logo_svg/light", filename)


@app.route("/api/predictions")
def predictions():
    try:
        model, strikeout_scaler, input_scalers, all_pitcher_scalers, all_batter_scalers = load_model_and_scaler()

        future_stats = get_future_stats()

        process_player_data = Process_player_data()
        processed_pitcher_stats, _ = process_player_data.process_pitcher_stats(future_stats)
        processed_batter_stats, _ = process_player_data.process_batter_stats(future_stats)

        X = np.column_stack(processed_pitcher_stats + processed_batter_stats)

        raw_predictions = model.predict(X, batch_size=1, verbose=0)
        scaled_up = strikeout_scaler.inverse_transform(raw_predictions)
        rounded = np.round(scaled_up)

        results = []
        for i in range(1, len(rounded)):   # skip boilerplate index 0
            team = future_stats[i][5] if len(future_stats[i]) > 5 else ""
            results.append({
                "name": future_stats[i][0],
                "k": round(float(rounded[i].item()), 2),
                "team": team
            })

        return jsonify({ "status": "ok", "predictions": results })

    except Exception as e:
        return jsonify({ "status": "error", "message": str(e) }), 500


'''if __name__ == "__main__":
    print("Starting server at http://localhost:10000")
    app.run(debug=False, port=5000)'''
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=10000)