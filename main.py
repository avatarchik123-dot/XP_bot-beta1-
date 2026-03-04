import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from engines.xp_engine import register_xp_handlers
from engines.reaction_handler import register_reaction_handlers
from engines.admin_engine import register_admin_handlers
from setup.wizard import register_wizard_handlers
from services.file_manager import init_files

TOKEN = "BOT_TOKEN"

async def main():
    init_files()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())

    register_xp_handlers(dp)
    register_reaction_handlers(dp)
    register_admin_handlers(dp)
    register_wizard_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())