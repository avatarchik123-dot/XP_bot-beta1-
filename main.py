import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from xp_engine import calculate_text_xp, calculate_media_xp, can_gain_xp
from level_engine import add_xp

# ====== ПУТИ И ПАПКИ ======
DATA_DIR = "data"
MEDIA_DIR = os.path.join(DATA_DIR, "media")
USER_DIR = os.path.join(DATA_DIR, "users")

for folder in [DATA_DIR, MEDIA_DIR, USER_DIR]:
    os.makedirs(folder, exist_ok=True)

# ====== ТОКЕН И БОТ ======
BOT_TOKEN = os.getenv("BOT_TOKEN")  # переменная Railway
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ====== ОБРАБОТЧИКИ ======

# Пример текстового XP
@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.reply("Бот готов к начислению XP!")

@dp.message()
async def gain_xp(message: types.Message):
    user_id = message.from_user.id
    text_xp = calculate_text_xp(message.text)
    media_xp = 0
    if message.photo or message.video or message.document:
        media_xp = calculate_media_xp(message)
    
    total_xp = text_xp + media_xp

    if can_gain_xp(user_id):
        add_xp(user_id, total_xp, USER_DIR)
        await message.reply(f"Вы получили {total_xp} XP!")

# ====== ЗАПУСК БОТА ======
async def main():
    from aiogram import F
    import asyncio

    try:
        print("Бот запускается...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())