from aiogram import types
from services.file_manager import load_json, save_json

# Функция для вычисления XP по тексту
def calculate_text_xp(message: types.Message) -> int:
    length = len(message.text or "")
    if length < 3:
        return 0
    if 3 <= length <= 9:
        return 1
    elif 10 <= length <= 29:
        return 2
    elif 30 <= length <= 49:
        return 3
    else:  # 50+
        return 5

# Функция для вычисления XP по медиа
def calculate_media_xp(message: types.Message) -> int:
    xp = 0
    if message.photo:
        xp += 3
    if message.video:
        xp += 5
    # Стикеры, GIF, голосовые = 0
    return xp

# Проверка, может ли юзер получать XP (антиспам)
def can_gain_xp(user_id: int, chat_id: int, last_times: dict) -> bool:
    import time
    last = last_times.get(str(chat_id), {}).get(str(user_id), 0)
    if time.time() - last >= 3:  # 3 секунды антифлуд
        return True
    return False

# Обновление последнего времени XP
def update_last_time(user_id: int, chat_id: int, last_times: dict):
    import time
    if str(chat_id) not in last_times:
        last_times[str(chat_id)] = {}
    last_times[str(chat_id)][str(user_id)] = time.time()
    return last_times