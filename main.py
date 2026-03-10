import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from engines.admin import router as admin_router
from engines.level import router as level_router
from engines.reaction import router as reaction_router
from setup.wizard import router as wizard_router
from services.pic import router as pic_router


async def main():

    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(wizard_router)
    dp.include_router(admin_router)
    dp.include_router(pic_router)
    dp.include_router(level_router)
    dp.include_router(reaction_router)
    

    print("It's alive")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())