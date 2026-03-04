import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Чтение токена из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Ошибка: переменная BOT_TOKEN не задана!")

# Убираем переносы и лишние пробелы
TOKEN = TOKEN.strip().replace("\n", "")

# Создаём объекты бота и диспетчера
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Простейший хендлер /start
@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await message.answer("Бот живой! Перейдите в личку для настройки.")

async def main():
    print("Старт бота...")
    try:
        # Проверим токен заранее
        me = await bot.get_me()
        print(f"Бот {me.username} активен")
    except Exception as e:
        print("Не удалось подключиться:", e)
        return

    from aiogram import F
    from aiogram import types

    # Запуск поллинга
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())