#!/bin/zsh
set -euo pipefail

# Cron has a minimal PATH; include common locations.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

cd /Users/spencerweishaar/personalProjects/baseball_predictions

python3 future_game_predictor.py

git add .

# Avoid failing when there is nothing new to commit.
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "daily update to stats and predictions"
git push origin main
