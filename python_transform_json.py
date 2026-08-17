#!/usr/bin/env python3
# json_to_csv.py
# Implements:
# 1. Open source of Json
# 2. Read Json
# 3. Convert to a csv format
# 4. Save csv format
# 5. Close Json

import json
import pandas as pd
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# -------- Configuration --------
# Option A: local JSON file
INPUT_JSON_PATH = Path("json/input.json")

# Option B: URL (comment out if not used)
# JSON_URL = "https://api.example.com/data"  

OUTPUT_CSV_PATH = Path("output/output.csv")
# -------------------------------

def read_json_from_file(path: Path):
    """Step 1 & 2: Open source of Json and Read Json (local file)"""
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data  # file is closed when leaving 'with' block

def read_json_from_url(url: str):
    """Alternate: read JSON directly from URL using requests"""
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def json_to_csv(data, out_path: Path):
    """Step 3 & 4: Convert to a CSV format and Save csv format.
    Uses pandas for convenience and handling of flat/mildly nested JSON.
    """
    # If data is a single dict (one record), wrap it so DataFrame becomes one row
    if isinstance(data, dict):
        # If there's a top-level key that contains the list of records, extract it:
        # common keys: 'data', 'results', 'items', etc. Adjust if needed.
        # Example check: if top-level has a list child, use that list.
        list_like = None
        for k, v in data.items():
            if isinstance(v, list):
                list_like = v
                break
        if list_like is not None:
            df = pd.json_normalize(list_like)
        else:
            df = pd.json_normalize(data)  # single-row dataframe
    elif isinstance(data, list):
        df = pd.json_normalize(data)
    else:
        raise ValueError("Unsupported JSON root type: {}".format(type(data)))

    # Save CSV (Step 4)
    df.to_csv(out_path, index=False, encoding="utf-8")

def main():
    # Choose source: file or URL
    if INPUT_JSON_PATH.exists():
        data = read_json_from_file(INPUT_JSON_PATH)
    else:
        # If using URL, uncomment JSON_URL above and use this:
        # data = read_json_from_url(JSON_URL)
        raise SystemExit(f"Input JSON file {INPUT_JSON_PATH} not found. Or enable URL path in script.")

    json_to_csv(data, OUTPUT_CSV_PATH)
    # Step 5: Close Json -> handled by context managers above (files/requests)
    print(f"Saved CSV to: {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    main()

    # Added this line to track it