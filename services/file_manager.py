import json
import os

DATA_DIR = "data"


def _path(filename: str):
    return os.path.join(DATA_DIR, filename)


def load_json(filename: str):
    path = _path(filename)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}


def save_json(filename: str, data: dict):
    path = _path(filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)