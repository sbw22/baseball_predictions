#!/bin/zsh
set -euo pipefail

# Cron has a minimal PATH; include common locations.
export PATH="/opt/anaconda3/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# Use the interpreter that has project dependencies installed.
PYTHON_BIN="/opt/anaconda3/bin/python3"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python3)"
fi

cd /Users/spencerweishaar/personalProjects/baseball_predictions

"$PYTHON_BIN" future_game_predictor.py

git add .

# Avoid failing when there is nothing new to commit.
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "daily update to stats and predictions"

# Cron cannot answer prompts; fail fast if auth is missing.
export GIT_TERMINAL_PROMPT=0
git push origin main
