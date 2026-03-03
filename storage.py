import json
import os
import shutil

FILES = [
    "groups.json",
    "levels.json",
    "levels_backup.json",
    "temp_setup.json"
]

def init_files():
    for file in FILES:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump({}, f)

def load(file):
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    if file == "levels.json":
        shutil.copyfile("levels.json", "levels_backup.json")
    with open(file, "w") as f:
        json.dump(data, f, indent=4)