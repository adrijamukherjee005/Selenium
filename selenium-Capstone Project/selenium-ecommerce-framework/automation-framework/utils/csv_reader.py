"""
Small helper for CSV-driven test data, used by both Unittest and PyTest suites.
"""
import csv
import os


def read_csv(relative_path):
    """Read a CSV under test_data/ and return a list of dicts (one per row)."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_dir, relative_path)
    with open(full_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
