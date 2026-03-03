import os

# Список нужных папок
folders = ["data", "data/profiles", "data/logs", "data/images", "data/backup"]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN
from storage import init_files
from xp_engine import calculate_text_xp, calculate_media_xp, can_gain_xp
from level_engine import add_xp

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        return
    if message.from_user.is_bot:
        return
    if not can_gain_xp(message.from_user.id):
        return

    text_xp = calculate_text_xp(message.text)
    media_xp = calculate_media_xp(message)
    total_xp = text_xp + media_xp

    if total_xp > 0:
        add_xp(message.chat.id, message.from_user.id, total_xp)

@dp.message(Command("rank"))
async def rank(message: Message):
    from level_engine import get_user_data
    user = get_user_data(message.chat.id, message.from_user.id)
    await message.answer(
        f"Уровень: {user['level']}\nXP: {user['xp']}"
    )

async def main():
    init_files()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())