# Baseball Strikeout Predictions

This project predicts how many strikeouts a starting pitcher will record in an MLB game.

It is organized as a full pipeline:

1. Collect and build training data from game and player stats.
2. Clean and scale that data so a model can learn from it.
3. Train a neural-network model.
4. Use the trained model to predict strikeouts for upcoming games.

The goal is to turn baseball stat tables into practical strikeout predictions that can be used for analysis and betting research.

## Project Structure

### Core pipeline files (detailed)

#### `creating_data.py`

This is the data-building script and one of the most important files in the project.

What it does:

- Pulls MLB game schedules and box scores (by date range and year range).
- Reads each game box score and extracts:
	- Starting pitcher name
	- Pitcher strikeout total (when available)
	- Opposing lineup (batter last names)
- Looks up advanced pitcher and batter stats from CSV files in `raw_betting_data/`.
- Converts text values to numbers.
- Averages opposing batter stats into one combined batter profile per pitcher/game.
- Writes all final records to `created_data/created_total_stats.csv`.

Why this file matters:

- It builds the training dataset used by everything downstream.
- If data quality is poor here, model quality will also be poor.

Main idea of the output row:

- Pitcher name
- Strikeouts in that game
- Year
- Pitcher advanced stats
- Averaged opposing batter stats

---

#### `process_data.py`

This file turns the raw created dataset into model-ready numeric arrays.

What it does:

- Loads `created_data/created_total_stats.csv`.
- Parses list-like text back into Python lists.
- Separates:
	- Target (`y`): pitcher strikeouts
	- Features (`X`): pitcher stats + batter stats
- Scales values with `MinMaxScaler` so different stats are on similar ranges.
- Saves processed artifacts:
	- `processed_data/X.joblib`
	- `processed_data/y.joblib`
	- scaler files in `model_and_scalers/`

Why this file matters:

- Machine-learning models usually train better when inputs are normalized.
- It also saves scalers so future predictions use the same value ranges as training.

---

#### `model.py`

This file defines, trains, evaluates, and saves the strikeout prediction model.

What it does:

- Loads processed `X` and `y` data from `processed_data/`.
- Splits data into training and testing sets.
- Builds a deep feedforward neural network (several dense layers, normalization, dropout).
- Trains with early stopping and checkpoint saving.
- Converts model outputs back from scaled values to real strikeout counts.
- Prints performance summaries (exact match, within 1, within 2, etc.).
- Saves:
	- Trained model file in `model_and_scalers/`
	- Evaluation CSV and heatmaps in `prediction_stats/`

Why this file matters:

- This is where learning actually happens.
- It also tracks how often predictions are close enough to be useful.

---

#### `future_game_predictor.py`

This file uses the trained model to predict strikeouts for upcoming (or same-day) games.

What it does:

- Loads the saved model and scaler files from `model_and_scalers/`.
- Collects current game data (pitchers + opposing batters).
- Reuses the same feature-building logic from `creating_data.py`.
- Reuses the same scaling logic from `process_data.py`.
- Creates model input and runs predictions.
- Prints pitcher-by-pitcher strikeout predictions.

Important implementation detail:

- It currently adds one "boilerplate" stat row so the feature shape matches what the model expects.
- This is a practical compatibility step in the current version of the project.

Why this file matters:

- It is the final "inference" step: where a trained model becomes usable for real games.

### Other Python files (brief)

- `basic_betting_plots.py`
	- Simple chart of American odds vs breakeven win percentage.
	- Useful for betting context and intuition.

- `player_spreads.py`
	- Sandbox script for reading player prop market data from a sportsbook API.
	- Mostly exploratory output/printing right now.

- `stat_correlations.py`
	- Exploratory analysis script.
	- Computes correlation between average pitcher strikeouts and individual stat columns.
	- Helps identify which stats may be useful model inputs.

## Data and model folders

- `raw_betting_data/`
	- Source CSV files (pitcher and batter stat tables collected from external sources).
	- These are the base inputs used to enrich game-level data.

- `created_data/`
	- Output of `creating_data.py`.
	- Contains assembled game-level dataset with pitcher result + feature lists.

- `processed_data/`
	- Output of `process_data.py`.
	- Contains model-ready feature matrix (`X`) and target vector (`y`).

- `model_and_scalers/`
	- Saved trained model(s) and scaler objects.
	- Needed to run consistent future predictions.

- `prediction_stats/`
	- Evaluation outputs from model testing.
	- Includes summary CSV and heatmap images.

## Typical Workflow

Run these scripts in order:

1. `python creating_data.py`
2. `python process_data.py`
3. `python model.py`
4. `python future_game_predictor.py`

## Dependencies

Main libraries used in this project include:

- `statsapi`
- `pybaseball`
- `numpy`
- `pandas`
- `scikit-learn`
- `tensorflow` / `keras`
- `matplotlib`
- `joblib`
- `requests`
- `beautifulsoup4`

## Notes

- This project is experimental and still evolving.
- Some scripts include exploratory/debug code paths.
- File names in `raw_betting_data/` include dates, so updating data sources may require adjusting paths in scripts.