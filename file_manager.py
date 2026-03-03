import os
import json
from config import GROUPS_FILE, LEVELS_FILE, LEVELS_BACKUP, TEMP_SETUP, MEDIA_FOLDER, USERS_FOLDER

def ensure_files_exist():
    for folder in [MEDIA_FOLDER, USERS_FOLDER]:
        os.makedirs(folder, exist_ok=True)
    for file in [GROUPS_FILE, LEVELS_FILE, TEMP_SETUP]:
        if not os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f:
                json.dump({}, f)

def read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    if path == LEVELS_FILE:
        # Бэкап перед сохранением
        if os.path.exists(LEVELS_FILE):
            backup = read_json(LEVELS_FILE)
            with open(LEVELS_BACKUP, "w", encoding="utf-8") as f:
                json.dump(backup, f, indent=4, ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)