"""Loads application configuration from config/config.json with environment overrides."""
import json
import os
from pathlib import Path
from typing import Any, Dict

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"

# Maps config keys to the environment variable that may override them.
_ENV_OVERRIDES = {
    "base_url": "BASE_URL",
    "browser": "BROWSER",
    "headless": "HEADLESS",
    "default_timeout_ms": "DEFAULT_TIMEOUT_MS",
}


def load_config() -> Dict[str, Any]:
    """Return the merged config: file defaults with any matching env vars applied on top."""
    with open(CONFIG_PATH, encoding="utf-8") as config_file:
        config = json.load(config_file)

    for key, env_var in _ENV_OVERRIDES.items():
        raw_value = os.getenv(env_var)
        if raw_value is None:
            continue
        if key == "headless":
            config[key] = raw_value.lower() not in ("false", "0", "no")
        elif key == "default_timeout_ms":
            config[key] = int(raw_value)
        else:
            config[key] = raw_value

    return config
