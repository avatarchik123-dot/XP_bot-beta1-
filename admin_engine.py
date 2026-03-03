from aiogram import types
from file_manager import read_json, write_json
from config import LEVELS_FILE, MAX_LOGS_PER_GROUP

def add_xp_admin(message: types.Message):
    # пример: /addxp @username 250
    args = message.get_args().split()
    if len(args) < 2:
        return message.answer("Неверный синтаксис")
    target = args[0]
    xp = int(args[1])
    # Заглушка
    return message.answer(f"{xp} XP добавлено пользователю {target}")

def remove_xp_admin(message: types.Message):
    args = message.get_args().split()
    if len(args) < 2:
        return message.answer("Неверный синтаксис")
    target = args[0]
    xp = int(args[1])
    return message.answer(f"{xp} XP удалено у пользователя {target}")

def show_logs(message: types.Message):
    return message.answer("Последние действия админов:\n(заглушка)")

def init_group(message: types.Message):
    group_id = message.chat.id
    # Создаем запись в LEVELS_FILE
    levels = read_json(LEVELS_FILE)
    if str(group_id) not in levels:
        levels[str(group_id)] = {}
    write_json(LEVELS_FILE, levels)
    return message.answer("Группа инициализирована.")