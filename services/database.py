import os
from tinydb import TinyDB, Query
from config import DATA_PATH

os.makedirs(DATA_PATH, exist_ok=True)

db = TinyDB(f"{DATA_PATH}/database.json")

# таблицы
users = db.table("users")
groups = db.table("groups")
reactions = db.table("reactions")
level_settings = db.table("level_settings")
level_names = db.table("level_names")
level_pics = db.table("level_pics")

User = Query()
Group = Query()
Reaction = Query()
Level = Query()


# ---------------- ГРУППЫ ----------------

def add_group(chat_id, title):

    if groups.contains(Group.chat_id == chat_id):

        groups.update(
            {"title": title},
            Group.chat_id == chat_id
        )

    else:

        groups.insert({
            "chat_id": chat_id,
            "title": title
        })


def get_groups():
    return groups.all()


# ---------------- НАСТРОЙКИ УРОВНЕЙ ----------------

def set_levels(chat_id, count):

    if level_settings.contains(Level.chat_id == chat_id):

        level_settings.update(
            {"levels": count},
            Level.chat_id == chat_id
        )

    else:

        level_settings.insert({
            "chat_id": chat_id,
            "levels": count,
            "distance": None
        })


def set_distance(chat_id, distance):

    if level_settings.contains(Level.chat_id == chat_id):

        level_settings.update(
            {"distance": distance},
            Level.chat_id == chat_id
        )

    else:

        level_settings.insert({
            "chat_id": chat_id,
            "levels": None,
            "distance": distance
        })


def get_settings(chat_id):

    result = level_settings.get(Level.chat_id == chat_id)

    if not result:
        return {}

    return result


# ---------------- НАЗВАНИЯ УРОВНЕЙ ----------------

def set_level_names(chat_id, names):

    level_names.remove(Level.chat_id == chat_id)

    for lvl, name in names.items():

        level_names.insert({
            "chat_id": chat_id,
            "level": lvl,
            "name": name
        })


def get_level_names(chat_id):

    data = level_names.search(Level.chat_id == chat_id)

    return {x["level"]: x["name"] for x in data}


# ---------------- КАРТИНКИ УРОВНЕЙ ----------------

def set_level_pic(chat_id, level, file_id):

    level_pics.remove(
        (Level.chat_id == chat_id) &
        (Level.level == level)
    )

    level_pics.insert({
        "chat_id": chat_id,
        "level": level,
        "file_id": file_id
    })


def get_level_pic(chat_id, level):

    data = level_pics.get(
        (Level.chat_id == chat_id) &
        (Level.level == level)
    )

    if data:
        return data["file_id"]

    return None


# ---------------- XP ПОЛЬЗОВАТЕЛЕЙ ----------------

def get_user(chat_id, user_id):

    user = users.get(
        (User.chat_id == chat_id) &
        (User.user_id == user_id)
    )

    if not user:

        user = {
            "chat_id": chat_id,
            "user_id": user_id,
            "xp": 0
        }

        users.insert(user)

    return user


def add_xp(chat_id, user_id, xp):

    user = get_user(chat_id, user_id)

    new_xp = user["xp"] + xp

    users.update(
        {"xp": new_xp},
        (User.chat_id == chat_id) &
        (User.user_id == user_id)
    )

    return new_xp


def remove_xp(chat_id, user_id, xp):

    user = get_user(chat_id, user_id)

    new_xp = max(0, user["xp"] - xp)

    users.update(
        {"xp": new_xp},
        (User.chat_id == chat_id) &
        (User.user_id == user_id)
    )

    return new_xp


def get_user_xp(chat_id, user_id):

    user = get_user(chat_id, user_id)

    return user["xp"]


def get_top_users(chat_id, limit=10):

    data = users.search(User.chat_id == chat_id)

    data.sort(key=lambda x: x["xp"], reverse=True)

    return data[:limit]