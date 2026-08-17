
#!/usr/bin/env python3
"""
process_salaries.py

Algorithm:
- Iterate through the data set.
- Save unique Names.
- Pick the name(s) that have more than one salary.
- For each such name, get the max salary.
- Print the name and the max salary.
"""

from collections import defaultdict
import sys

def find_max_salaries(records):
    """
    records: iterable of (name, salary) pairs
    returns: dict { name: max_salary } for names that have >1 salary entry
    """
    salaries_by_name = defaultdict(list)
    for name, salary in records:
        # normalize name (strip whitespace)
        key = str(name).strip()
        try:
            num = float(salary)
        except (TypeError, ValueError):
            # skip non-numeric salaries
            continue
        salaries_by_name[key].append(num)

    # keep only names with more than one salary, compute max
    result = {}
    for name, sal_list in salaries_by_name.items():
        if len(sal_list) > 1:
            result[name] = max(sal_list)
    return result

def main():
    # Example dataset: list of (name, salary)
    data = [
        ("John", 50000),
        ("Jane", 70000),
        ("John", 55000),
        ("Alice", 48000),
        ("Jane", 72000),
        ("Bob", 60000),
    ]

    # If you want to accept CSV input from a file, implement parsing here.
    # For now we use the example `data`.
    results = find_max_salaries(data)

    if not results:
        print("No names have more than one salary entry.")
        return

    for name, max_salary in results.items():
        print(f"{name}: {max_salary}")

if __name__ == "__main__":
    main()