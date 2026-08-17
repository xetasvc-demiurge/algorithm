from algorithm import find_max_salaries


def test_returns_max_salary_only_for_repeated_names():
    data = [
        ("John", 50000),
        ("Jane", 70000),
        ("John", 55000),
        ("Alice", 48000),
        ("Jane", 72000),
        ("Bob", 60000),
    ]
    assert find_max_salaries(data) == {"John": 55000.0, "Jane": 72000.0}


def test_empty_input_returns_empty_dict():
    assert find_max_salaries([]) == {}


def test_all_unique_names_returns_empty_dict():
    assert find_max_salaries([("John", 1), ("Jane", 2)]) == {}


def test_skips_non_numeric_salary():
    data = [("John", 50000), ("John", "not-a-number")]
    assert find_max_salaries(data) == {}
