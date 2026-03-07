import os
from tinydb import TinyDB, Query
from config import DATA_PATH

os.makedirs(DATA_PATH, exist_ok=True)

db = TinyDB(f"{DATA_PATH}/database.json")

users = db.table("users")
groups = db.table("groups")
reactions = db.table("reactions")

User = Query()
Group = Query()
Reaction = Query()