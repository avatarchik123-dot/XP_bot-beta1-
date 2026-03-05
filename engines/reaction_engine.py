from services.file_manager import load_json, save_json

# Начисление XP за реакцию
def add_reaction_xp(chat_id: int, message_id: int, user_id: int):
    levels = load_json("levels")
    if str(chat_id) not in levels:
        levels[str(chat_id)] = {}
    user_data = levels[str(chat_id)].get(str(user_id), {"xp": 0, "level": 0})

    # Лимит 50 XP на сообщение
    msg_key = f"{message_id}_reactions"
    reactions = user_data.get(msg_key, 0)
    if reactions < 50:
        user_data["xp"] += 1
        user_data[msg_key] = reactions + 1

    levels[str(chat_id)][str(user_id)] = user_data
    save_json("levels", levels)
    return user_data