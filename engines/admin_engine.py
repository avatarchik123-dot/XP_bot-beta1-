from services.file_manager import load_json, save_json

def add_xp_admin(chat_id: int, user_id: int, xp: int, self_action=False):
    levels = load_json("levels")
    if str(chat_id) not in levels:
        levels[str(chat_id)] = {}
    user_data = levels[str(chat_id)].get(str(user_id), {"xp": 0, "level": 0})
    user_data["xp"] += xp
    levels[str(chat_id)][str(user_id)] = user_data
    save_json("levels", levels)

    # Логируем действие
    logs = load_json("groups")
    if str(chat_id) not in logs:
        logs[str(chat_id)] = []
    log_entry = {"user_id": user_id, "xp": xp, "self_action": self_action}
    logs[str(chat_id)].append(log_entry)
    # Храним только последние 100 записей
    logs[str(chat_id)] = logs[str(chat_id)][-100:]
    save_json("groups", logs)
    return user_data