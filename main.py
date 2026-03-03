import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN
from xp_engine import calculate_text_xp, calculate_media_xp, can_gain_xp
from level_engine import add_xp, get_level_info
from reaction_engine import process_reaction
from admin_engine import is_admin, execute_admin_command
from cache_engine import cache_set, cache_get

# --- Настройка директорий ---
required_dirs = ["data", "logs", "cache"]
for d in required_dirs:
    if not os.path.exists(d):
        os.makedirs(d)

# --- Инициализация бота ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Хэндлер старт ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Бот готов к начислению ХР.")

# --- Основной хэндлер сообщений ---
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text_xp = calculate_text_xp(message.text) if message.text else 0
    media_xp = calculate_media_xp(message) if message.photo or message.video else 0
    total_xp = text_xp + media_xp

    if can_gain_xp(user_id):
        new_level = add_xp(user_id, total_xp)
        if new_level:
            await message.answer(f"Поздравляю! Ты достиг уровня {new_level} 🎉")

    # Реакции на текст и медиа
    await process_reaction(message)

# --- Админ-команды ---
@dp.message()
async def admin_commands(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    if message.text.startswith("/admin"):
        result = execute_admin_command(message.text, message.from_user.id)
        await message.answer(result)

# --- Кэширование (пример) ---
@dp.message()
async def cache_example(message: types.Message):
    if message.text.startswith("/cache"):
        key = message.text.split()[1]
        value = cache_get(key)
        await message.answer(f"Значение из кэша: {value}")

# --- Запуск бота ---
async def main():
    print("Бот запускается...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())