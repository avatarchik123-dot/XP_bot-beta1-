from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.utils import executor

from xp_engine import calculate_text_xp, calculate_media_xp, can_gain_xp
from level_engine import add_xp

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # токен из .env

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Проверка/создание необходимых папок
required_dirs = ["data", "logs", "backups"]
for d in required_dirs:
    if not os.path.exists(d):
        os.makedirs(d)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Бот живой!")

# Обработчик любых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    # пример подсчёта ХР
    text_xp = calculate_text_xp(message.text)
    media_xp = calculate_media_xp(message)
    total_xp = text_xp + media_xp

    # добавить ХР в уровень
    add_xp(message.from_user.id, total_xp)

    # ответ для проверки
    await message.reply(f"Вы получили {total_xp} XP!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)