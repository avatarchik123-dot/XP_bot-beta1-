# main.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types

from xp_engine import calculate_text_xp, calculate_media_xp, can_gain_xp
from level_engine import add_xp, get_level_info
from reaction_engine import process_reaction
from admin_engine import is_admin
from cache_engine import Cache

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
cache = Cache()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Бот готов к начислению XP!")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text_xp = calculate_text_xp(message.text)
    media_xp = calculate_media_xp(message)
    if can_gain_xp(user_id):
        new_level = add_xp(user_id, text_xp + media_xp)
        if new_level:
            await message.reply(f"Поздравляем! Вы достигли уровня {new_level}.")
    await process_reaction(message)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())