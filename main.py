import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import *
from file_manager import ensure_files_exist, read_json, write_json
from xp_engine import calculate_text_xp, calculate_media_xp, can_gain_xp
from level_engine import add_xp, get_level_info, check_level_up
from reaction_engine import on_reaction
from admin_engine import add_xp_admin, remove_xp_admin, show_logs, init_group
from wizard import start_wizard
from cache_manager import get_top_cache, update_top_cache

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Убедимся, что все файлы/папки созданы
ensure_files_exist()

user_last_message = {}  # для антиспама
user_last_text = {}     # для антифарм

### ЛИЧКА /start ###
@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("➕ Добавить в группу")],
            [KeyboardButton("⚙️ Настроить бота")],
            [KeyboardButton("📂 Мои группы")]
        ],
        resize_keyboard=True
    )
    await message.answer("Привет! Выберите действие:", reply_markup=keyboard)

### INIT GROUP ###
@dp.message(Command("initgroup"))
async def init_group_command(message: types.Message):
    await init_group(message)

### RANK ###
@dp.message(Command("rank"))
async def rank_command(message: types.Message):
    args = message.get_args().split()
    target_id = None
    if args:
        # упрощённо: получаем user_id через username
        # Реализация поиска user_id по username должна быть через API Telegram
        await message.answer("Функция на username пока заглушка")
        return
    else:
        target_id = message.from_user.id

    group_id = message.chat.id
    info = get_level_info(target_id, group_id)
    progress_bar = "█" * (info['progress_percent'] // 10) + "░" * (10 - info['progress_percent'] // 10)
    await message.answer(f"Уровень: {info['level']}\nXP: {info['xp']}/{info['xp_next']}\n[{progress_bar}]")

### TOP ###
@dp.message(Command("top"))
async def top_command(message: types.Message):
    group_id = message.chat.id
    data = get_top_cache(group_id)
    if not data:
        # Формируем топ
        # Заглушка
        data = "Топ 5 участников:\n1. Пользователь1 — 300 XP\n2. Пользователь2 — 250 XP\n..."
        update_top_cache(group_id, data)
    await message.answer(data)

### ADDXP / REMOVEXP ###
@dp.message(Command("addxp"))
async def addxp_command(message: types.Message):
    await add_xp_admin(message)

@dp.message(Command("removexp"))
async def removexp_command(message: types.Message):
    await remove_xp_admin(message)

### LOGS ###
@dp.message(Command("logs"))
async def logs_command(message: types.Message):
    await show_logs(message)

### Начисление XP за сообщения ###
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    group_id = message.chat.id

    # Игнорируем
    if message.from_user.is_bot or message.text is None or len(message.text) < 3 or message.text.startswith("/"):
        return

    # Антиспам 3 сек
    last_time = user_last_message.get((user_id, group_id))
    now = asyncio.get_event_loop().time()
    if last_time and now - last_time < ANTI_SPAM_SECONDS:
        return
    user_last_message[(user_id, group_id)] = now

    # Антифарм 3 одинаковых
    last_texts = user_last_text.get((user_id, group_id), [])
    last_texts.append(message.text)
    if len(last_texts) > 3:
        last_texts.pop(0)
    user_last_text[(user_id, group_id)] = last_texts
    if len(last_texts) == 3 and last_texts[0] == last_texts[1] == last_texts[2]:
        return

    xp = calculate_text_xp(message.text)
    xp += calculate_media_xp(message)
    add_xp(user_id, group_id, xp)

    await check_level_up(user_id, group_id, bot)

### Реакции ###
@dp.message()
async def handle_reactions(message: types.Message):
    # placeholder: на Reactions API
    pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())