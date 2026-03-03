import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from xp_engine import calculate_text_xp, calculate_media_xp, can_gain_xp
from level_engine import add_xp
from dotenv import load_dotenv

# Загружаем .env (если он есть, не критично)
load_dotenv()

# Токен берём из переменной окружения Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда старт для проверки
@dp.message(Command("start"))
async def start_test(message: types.Message):
    await message.reply("Бот живой!")

# Обработчик сообщений для начисления XP
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text_xp = calculate_text_xp(message.text)
    media_xp = calculate_media_xp(message)
    if can_gain_xp(user_id):
        add_xp(user_id, text_xp + media_xp)

# Точка входа
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))