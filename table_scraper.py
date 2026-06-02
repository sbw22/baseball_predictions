"""
Scrapes the Baseball Savant Custom Leaderboard for batters AND pitchers
across multiple years, saving one CSV per player type with all years combined.

The leaderboard page loads data client-side, so we try three strategies:
  1. CSV download (?csv=true)
  2. JSON via Accept header
  3. HTML parse for an embedded JS variable

ADJUSTABLE SETTINGS:
  - YEARS  : list of seasons to pull
  - MIN_PA : minimum plate appearances for batters ("q" = qualified, or int)
  - MIN_IP : minimum innings pitched for pitchers ("q" = qualified, or int)
"""

import io, re, json, time
import requests
import pandas as pd
from datetime import date

# ── CONFIG ─────────────────────────────────────────────────────────────────────
YEARS  = list(range(2016, 2027))   # 2016 through 2026 inclusive
MIN_PA = 20    # batters:  "q" for qualified, or an integer e.g. 100
MIN_IP = 20    # pitchers: "q" for qualified, or an integer e.g. 50
# ──────────────────────────────────────────────────────────────────────────────

BASE_URL = "https://baseballsavant.mlb.com/leaderboard/custom"

HEADERS = {
    "User-Agent":      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36",
    "Accept":          "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer":         "https://baseballsavant.mlb.com/",
}

# API field names for each player type, in CSV column order.
# These match the column headers in the reference CSV files exactly.
BATTER_SELECTIONS = ",".join([
    "ab", "pa", "hit", "single", "double",
    "k_percent", "bb_percent", "batting_avg", "slg_percent",
    "on_base_percent", "on_base_plus_slg", "b_rbi", "b_total_bases",
    "b_ab_scoring", "b_gnd_into_dp", "b_gnd_into_tp",
    "b_hit_ground", "b_hit_fly", "b_hit_line_drive", "b_hit_popup",
    "b_out_ground", "b_out_line_drive", "b_out_popup",
    "b_played_dh", "b_sac_fly", "b_swinging_strike",
    "r_interference", "r_pickoff_1b", "r_pickoff_2b",
    "r_run", "b_total_sacrifices", "b_reached_on_error",
    "xslg", "xwoba", "wobacon", "xwobacon", "bacon",
    "xbadiff", "xslgdiff", "wobadiff",
    "barrel", "avg_best_speed", "whiff_percent", "swing_percent",
])

PITCHER_SELECTIONS = ",".join([
    "pa", "ab", "strikeout", "k_percent", "bb_percent",
    "batting_avg", "slg_percent", "on_base_percent", "on_base_plus_slg",
    "isolated_power", "babip", "xba", "xslg", "woba", "xwoba",
    "xobp", "xiso", "wobacon", "xwobacon", "bacon", "xbacon",
    "exit_velocity_avg", "sweet_spot_percent", "solidcontact_percent",
    "hard_hit_percent", "avg_hyper_speed", "whiff_percent",
])

# TODAY = date.today().strftime("%m-%d-%Y")
TODAY = "current" # We are excluding the date from the file name for the stats, due to the github action being in a different time zone (might fix this later)

# (api_type, min_value, sort_dir, selections, output_filename)
PLAYER_TYPES = [
    ("batter",  MIN_PA, "desc", BATTER_SELECTIONS,  f"all_batters_{TODAY}.csv"),
    ("pitcher", MIN_IP, "asc",  PITCHER_SELECTIONS, f"all_pitchers_{TODAY}.csv"),
]


def build_params(player_type, year, min_val, sort_dir, selections):
    return {
        "year":       year,
        "type":       player_type,
        "filter":     "",
        "min":        min_val,
        "selections": selections,
        "chart":      "false",
        "x": "pa", "y": "pa", "r": "no",
        "chartType":  "beeswarm",
        "sort":       "xwoba",
        "sortDir":    sort_dir,
    }


def try_csv_download(player_type, year, min_val, sort_dir, selections):
    """Strategy 1: direct CSV download via &csv=true."""
    params = build_params(player_type, year, min_val, sort_dir, selections)
    params["csv"] = "true"
    r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
    if r.status_code == 200 and "text/csv" in r.headers.get("content-type", ""):
        return pd.read_csv(io.StringIO(r.text))
    return None


def try_json_endpoint(player_type, year, min_val, sort_dir, selections):
    """Strategy 2: request JSON explicitly via Accept/XHR headers."""
    hdrs = {**HEADERS, "Accept": "application/json", "X-Requested-With": "XMLHttpRequest"}
    params = build_params(player_type, year, min_val, sort_dir, selections)
    r = requests.get(BASE_URL, params=params, headers=hdrs, timeout=30)
    if r.status_code == 200 and r.text.strip().startswith(("[", "{")):
        payload = r.json()
        rows = payload["data"] if isinstance(payload, dict) else payload
        return pd.DataFrame(rows)
    return None


def try_html_parse(player_type, year, min_val, sort_dir, selections):
    """Strategy 3: fetch the HTML page and extract the embedded JS data array."""
    params = build_params(player_type, year, min_val, sort_dir, selections)
    r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
    for var in ["playersData", "leaderboard_data", "data", "players"]:
        m = re.search(rf'var\s+{var}\s*=\s*(\[.*?\])\s*;', r.text, re.DOTALL)
        if m:
            return pd.DataFrame(json.loads(m.group(1)))
    # Last resort: find any JS array assignment
    m = re.search(r'=\s*(\[\s*\{.*?\}\s*\])\s*;', r.text, re.DOTALL)
    if m:
        return pd.DataFrame(json.loads(m.group(1)))
    print(f"    !! Could not parse HTML for {player_type} {year}. "
          f"First 800 chars:\n{r.text[:800]}")
    return None


def fetch_year(player_type, year, min_val, sort_dir, selections):
    """Try each strategy in order; return a DataFrame or raise."""
    for strategy in (try_csv_download, try_json_endpoint, try_html_parse):
        df = strategy(player_type, year, min_val, sort_dir, selections)
        if df is not None and not df.empty:
            return df
    raise RuntimeError(f"All strategies failed for {player_type} {year}.")


def normalize(df, year):
    """Combine name columns and add year, matching reference CSV structure."""
    if "last_name" in df.columns and "first_name" in df.columns:
        df["last_name, first_name"] = df["last_name"] + ", " + df["first_name"]
        df.drop(columns=["last_name", "first_name"], inplace=True)
    df["year"] = year  # ensure year column is present
    # Put identifying columns first
    front = [c for c in ["last_name, first_name", "player_id", "year"] if c in df.columns]
    rest  = [c for c in df.columns if c not in front]
    return df[front + rest]


# ── MAIN LOOP: fetch all years, combine, save ──────────────────────────────────
for player_type, min_val, sort_dir, selections, output_file in PLAYER_TYPES:
    print(f"\n{'='*50}\nFetching {player_type}s for {len(YEARS)} years...\n{'='*50}")
    frames = []
    for year in YEARS:
        df = fetch_year(player_type, year, min_val, sort_dir, selections)
        df = normalize(df, year)
        frames.append(df)
        print(f"  {year}: {len(df)} rows")
        time.sleep(0.5)   # be polite — avoid hammering the server

    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(f"raw_betting_data/{output_file}", index=False)
    print(f"\n  → {len(combined)} total rows saved to raw_betting_data/{output_file}")