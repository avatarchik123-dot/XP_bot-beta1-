import json
import os
from datetime import datetime

# Пути к основным JSON-файлам
DATA_PATH = "./data"  # папка, где хранятся все json
FILES = {
    "groups": os.path.join(DATA_PATH, "groups.json"),
    "levels": os.path.join(DATA_PATH, "levels.json"),
    "levels_backup": os.path.join(DATA_PATH, "levels_backup.json"),
    "temp_setup": os.path.join(DATA_PATH, "temp_setup.json"),
    "load": os.path.join(DATA_PATH, "load.json")
}

def ensure_data_folder():
    """Создает папку для данных, если её нет"""
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

def ensure_files():
    """Создает файлы, если их нет, с пустым словарем"""
    ensure_data_folder()
    for key, path in FILES.items():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)

def load_json(file_key):
    """Загрузить данные из JSON файла"""
    ensure_files()
    path = FILES[file_key]
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Если файл поврежден, сбросим в пустой словарь
        return {}

def save_json(file_key, data):
    """Сохранить данные в JSON с бэкапом"""
    ensure_files()
    path = FILES[file_key]

    # Создаем бэкап
    if os.path.exists(path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{FILES['levels_backup'].replace('.json','')}_{timestamp}.json"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Сохраняем текущие данные
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)