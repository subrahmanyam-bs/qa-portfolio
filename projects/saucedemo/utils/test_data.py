"""Loads test fixture data (users, products, checkout data) from test_data/test_data.json."""
import json
from pathlib import Path
from typing import Any, Dict

TEST_DATA_PATH = Path(__file__).resolve().parent.parent / "test_data" / "test_data.json"


def load_test_data() -> Dict[str, Any]:
    """Return the full test data dictionary, loaded fresh from disk."""
    with open(TEST_DATA_PATH, encoding="utf-8") as data_file:
        return json.load(data_file)
