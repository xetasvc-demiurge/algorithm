import csv

from loading_csv import compute_stats, safe_float


def test_safe_float_valid_and_invalid():
    assert safe_float("42.5") == 42.5
    assert safe_float("not-a-number") is None
    assert safe_float(None) is None


def test_compute_stats_basic(tmp_path):
    csv_path = tmp_path / "data.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["salary"])
        writer.writeheader()
        for value in ("10", "20", "30"):
            writer.writerow({"salary": value})

    stats = compute_stats(csv_path, numeric_columns=["salary"])
    s = stats["salary"]
    assert s["count"] == 3
    assert s["sum"] == 60.0
    assert s["min"] == 10.0
    assert s["max"] == 30.0
    assert s["mean"] == 20.0
    assert s["median"] == 20.0


def test_compute_stats_skips_non_numeric(tmp_path):
    csv_path = tmp_path / "data.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["salary"])
        writer.writeheader()
        writer.writerow({"salary": "n/a"})
        writer.writerow({"salary": "50"})

    stats = compute_stats(csv_path, numeric_columns=["salary"])
    assert stats["salary"]["count"] == 1
    assert stats["salary"]["sum"] == 50.0


def test_compute_stats_no_numeric_data(tmp_path):
    csv_path = tmp_path / "data.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["salary"])
        writer.writeheader()
        writer.writerow({"salary": "n/a"})

    stats = compute_stats(csv_path, numeric_columns=["salary"])
    assert stats["salary"]["count"] == 0
