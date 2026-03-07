import os
from tinydb import TinyDB

DATA_PATH = os.getenv("DATA_PATH", "./data")
os.makedirs(DATA_PATH, exist_ok=True)

db = TinyDB(f"{DATA_PATH}/database.json")