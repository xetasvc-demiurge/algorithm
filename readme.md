# Hippo Digital — Python Data Exercises

Small standalone Python scripts for data-wrangling practice:

- `algorithm.py` — find the max salary for names that appear more than once in a dataset.
- `python_API_function.py` — calls an API with retry/backoff, timeout, and error handling.
- `python_transform_json.py` — reads JSON and converts it to CSV.
- `loading_csv.py` — reads a CSV and computes basic statistics (count, sum, min, max, mean, median, stdev).

## Setup

```bash
python -m venv .venv
.venv/Scripts/activate        # or source .venv/bin/activate on macOS/Linux
pip install -r requirements-dev.txt
