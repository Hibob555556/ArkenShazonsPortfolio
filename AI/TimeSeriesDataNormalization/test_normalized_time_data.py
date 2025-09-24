import pytest
import pandas as pd
import os

csv_file = "time_encoding.csv"

# -----------------------------
# Fixture to load CSV once
# -----------------------------
@pytest.fixture(scope="module")
def df():
    if not os.path.exists(csv_file):
        pytest.skip(f"{csv_file} does not exist, skipping tests.")
    return pd.read_csv(csv_file)

# -----------------------------
# Tests
# -----------------------------

def test_csv_exists():
    assert os.path.exists(csv_file), f"{csv_file} does not exist!"

def test_csv_columns(df):
    expected_columns = ["day", "minute", "day_sin", "day_cos", "time_sin", "time_cos", "normalized_value"]
    assert list(df.columns) == expected_columns

def check_for_duplicates(df):
    """Return 1 if no duplicate rows, 0 otherwise."""
    duplicates = df[df.duplicated(keep=False)]
    return 1 if duplicates.empty else 0

def test_csv_output(df):
    assert check_for_duplicates(df) == 1

def test_value_ranges(df):
    # Check cyclical features are within [-1, 1]
    for col in ["day_sin", "day_cos", "time_sin", "time_cos"]:
        assert df[col].between(-1, 1).all()
    # Check normalized_value is within [0, 1]
    assert df["normalized_value"].between(0, 1).all()

def test_row_count(df):
    # Ensure exactly 365 days × 1440 minutes
    assert len(df) == 365 * 1440

def test_unique_day_minute(df):
    # Ensure no duplicate day/minute combinations
    assert df.duplicated(subset=["day", "minute"]).sum() == 0

# -----------------------------
# Allow direct execution
# -----------------------------
if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
