import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from engines.admin_engine import router as admin_router
from engines.level_engine import router as level_router
from engines.reaction_engine import router as reaction_router
from engines.xp_engine import router as xp_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(admin_router)
    dp.include_router(level_router)
    dp.include_router(reaction_router)
    dp.include_router(xp_router)

    print("Bot started")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

    print("deploy test 123")