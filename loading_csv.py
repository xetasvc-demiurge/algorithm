# get_open_read_calculate_stats.py
# Basic script
#
# Algorithm labels:
# 1) Get source of a csv       -> provide the CSV file path (csv_path)
# 2) Open the csv              -> open(...) or csv.reader
# 3) Read through the csv      -> iterate rows
# 4) Calculate it's statistics -> count, sum, min, max, mean for numeric columns
#
# This script calculates simple statistics for one numeric column (default: "Salary").
# It's beginner-friendly and uses the csv module only.

import csv
import math
from collections import defaultdict

CSV_PATH = "csv/data.csv"  # 1) Get source of a csv - change this to your file path
NUMERIC_COLUMNS = ["salary"]  # column(s) to compute statistics for; update as needed

def safe_float(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None

def main(csv_path):
    # 2) Open the csv
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Prepare accumulators for each numeric column
        stats = {}
        for col in NUMERIC_COLUMNS:
            stats[col] = {
                "count": 0,
                "sum": 0.0,
                "min": math.inf,
                "max": -math.inf,
                "values": [],  # keep values for mean/median if desired; remove for memory savings
            }

        # 3) Read through the csv
        for row in reader:
            for col in NUMERIC_COLUMNS:
                raw = row.get(col)
                val = safe_float(raw)
                if val is None:
                    continue  # skip missing / non-numeric

                # 4) Calculate it's statistics (update accumulators)
                s = stats[col]
                s["count"] += 1
                s["sum"] += val
                if val < s["min"]:
                    s["min"] = val
                if val > s["max"]:
                    s["max"] = val
                s["values"].append(val)  # optional: keep values for median, stdev

        # Print results
        for col, s in stats.items():
            print(f"Column: {col}")
            if s["count"] == 0:
                print("  No numeric data found.")
                continue
            mean = s["sum"] / s["count"]
            # median example (simple)
            values_sorted = sorted(s["values"])
            mid = s["count"] // 2
            if s["count"] % 2 == 1:
                median = values_sorted[mid]
            else:
                median = (values_sorted[mid - 1] + values_sorted[mid]) / 2
            # simple population variance / stdev (sample stdev would divide by count-1)
            var = sum((x - mean) ** 2 for x in s["values"]) / s["count"]
            stdev = math.sqrt(var)

            print(f"  count: {s['count']}")
            print(f"  sum: {s['sum']}")
            print(f"  min: {s['min']}")
            print(f"  max: {s['max']}")
            print(f"  mean: {mean}")
            print(f"  median: {median}")
            print(f"  stdev (population): {stdev}")

if __name__ == "__main__":
    main(CSV_PATH)