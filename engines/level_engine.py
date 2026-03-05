from services.file_manager import load_json, save_json

# Добавляем XP пользователю
def add_xp(chat_id: int, user_id: int, xp: int):
    levels = load_json("levels")
    if str(chat_id) not in levels:
        levels[str(chat_id)] = {}
    user_data = levels[str(chat_id)].get(str(user_id), {"xp": 0, "level": 0})
    user_data["xp"] += xp
    levels[str(chat_id)][str(user_id)] = user_data
    save_json("levels", levels)
    return user_data

# Получаем информацию о уровне
def get_level_info(chat_id: int, user_id: int):
    levels = load_json("levels")
    return levels.get(str(chat_id), {}).get(str(user_id), {"xp": 0, "level": 0})