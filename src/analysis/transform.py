import json
from pathlib import Path

OVERRIDE_PATH = Path("data/config/override-type.json")

def load_overrides() -> dict[str, str]:
    if not OVERRIDE_PATH.exists():
        return {}
    with open(OVERRIDE_PATH, "r") as f:
        return json.load(f)
