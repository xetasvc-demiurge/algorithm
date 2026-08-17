import json

import pandas as pd  # pyright: ignore[reportMissingImports]
import pytest

from python_transform_json import json_to_csv, read_json_from_file


def test_read_json_from_file(tmp_path):
    data = [{"a": 1}, {"a": 2}]
    json_path = tmp_path / "input.json"
    json_path.write_text(json.dumps(data), encoding="utf-8")
    assert read_json_from_file(json_path) == data


def test_json_to_csv_with_list_root(tmp_path):
    data = [{"name": "John", "salary": 50000}, {"name": "Jane", "salary": 60000}]
    out_path = tmp_path / "output.csv"
    json_to_csv(data, out_path)
    df = pd.read_csv(out_path)
    assert list(df["name"]) == ["John", "Jane"]
    assert list(df["salary"]) == [50000, 60000]


def test_json_to_csv_with_dict_root_containing_list(tmp_path):
    data = {"results": [{"name": "John"}, {"name": "Jane"}]}
    out_path = tmp_path / "output.csv"
    json_to_csv(data, out_path)
    df = pd.read_csv(out_path)
    assert list(df["name"]) == ["John", "Jane"]


def test_json_to_csv_rejects_unsupported_root(tmp_path):
    with pytest.raises(ValueError):
        json_to_csv("not-a-dict-or-list", tmp_path / "output.csv")
