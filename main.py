import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from engines.admin import router as admin_router
from engines.level import router as level_router
from engines.xp import router as xp_router
from engines.reaction import router as reaction_router


async def main():

    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()

    app.include_router(admin_router)
    app.include_router(level_router)
    app.include_router(xp_router)
    app.include_router(reaction_router)

    print("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())