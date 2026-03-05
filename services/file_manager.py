import json
import os

DATA_PATH = "data"


def _path(name):
    return os.path.join(DATA_PATH, name)


def load_json(filename):
    path = _path(filename)

    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({}, f)

    with open(path, "r") as f:
        return json.load(f)


def save_json(filename, data):
    path = _path(filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def update_json(filename, key, value):
    data = load_json(filename)
    data[key] = value
    save_json(filename, data)