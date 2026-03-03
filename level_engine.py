from file_manager import read_json, write_json
from config import LEVELS_FILE, MAX_REACTION_XP

def add_xp(user_id, group_id, xp):
    levels = read_json(LEVELS_FILE)
    if str(group_id) not in levels:
        levels[str(group_id)] = {}
    user_data = levels[str(group_id)].get(str(user_id), {"xp": 0, "level": 0})
    user_data["xp"] += xp
    levels[str(group_id)][str(user_id)] = user_data
    write_json(LEVELS_FILE, levels)

def get_level_info(user_id, group_id):
    levels = read_json(LEVELS_FILE)
    group = levels.get(str(group_id), {})
    user = group.get(str(user_id), {"xp": 0, "level": 0})
    xp_next = user["level"] * 100 + 100  # Пример
    progress_percent = int(user["xp"] / xp_next * 100) if xp_next else 100
    return {"level": user["level"], "xp": user["xp"], "xp_next": xp_next, "progress_percent": progress_percent}

async def check_level_up(user_id, group_id, bot):
    info = get_level_info(user_id, group_id)
    # Заглушка уведомления
    if info["xp"] >= info["xp_next"]:
        info["level"] += 1
        # Обновляем
        levels = read_json(LEVELS_FILE)
        levels[str(group_id)][str(user_id)] = {"xp": info["xp"], "level": info["level"]}
        write_json(LEVELS_FILE, levels)
        await bot.send_message(user_id, f"Поздравляем! Новый уровень: {info['level']}")