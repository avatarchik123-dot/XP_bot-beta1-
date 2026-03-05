import json
import os
import shutil

DATA = [
    "groups.json",
    "levels.json",
    "levels_backup.json",
    "temp_setup.json"
]

def init_files():
    os.makedirs("data", exist_ok=True)
    for file in DATA_FILES:
        path = f"data/{file}"
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({}, f)

def load(file):
    with open(f"data/{file}", "r") as f:
        return json.load(f)

def save(file, data):
    if file == "levels.json":
        shutil.copy("data/levels.json", "data/levels_backup.json")

    with open(f"data/{file}", "w") as f:
        json.dump(data, f, indent=4)