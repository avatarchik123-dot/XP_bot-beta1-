import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN

# engines
from engines import xp_engine
from engines import level_engine
from engines import reaction_engine
from engines import admin_engine


async def main():

    token = os.getenv("BOT_TOKEN") or BOT_TOKEN

    if not token:
        raise ValueError("BOT_TOKEN not found")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    # подключаем engines
    dp.include_router(xp_engine.router)
    dp.include_router(level_engine.router)
    dp.include_router(reaction_engine.router)
    dp.include_router(admin_engine.router)

    print("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())