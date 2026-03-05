import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Импорт роутеров энжинов
from engines.xp_engine import xp_router
from engines.level_engine import level_router
from engines.reaction_engine import reaction_router
from engines.admin_engine import admin_router

# Импорт менеджеров
from services.file_manager import FileManager
from services.cache_manager import CacheManager

# Импорт конфигов
from config import BOT_TOKEN  # Если BOT_TOKEN нет в переменных среды, берем из конфигов

# Инициализация менеджеров
file_manager = FileManager()
cache_manager = CacheManager()

# Проверка токена
TOKEN = os.getenv("BOT_TOKEN") or BOT_TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Подключаем роутеры
dp.include_router(xp_router)
dp.include_router(level_router)
dp.include_router(reaction_router)
dp.include_router(admin_router)

# Стартовый хэндлер
@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    kb = InlineKeyboardBuilder()
    kb.add(*[
        kb.button(text="➕ Добавить в группу"),
        kb.button(text="⚙️ Настроить бота"),
        kb.button(text="📂 Мои группы")
    ])
    await message.answer("Бот живой! Выберите действие:", reply_markup=kb.as_markup())

async def main():
    # Создаем нужные папки и файлы при старте
    await file_manager.ensure_structure()
    print("Файловая структура готова.")
    
    # Запуск бота
    print("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")