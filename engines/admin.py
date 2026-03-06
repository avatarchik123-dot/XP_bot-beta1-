from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.file_manager import db

router = Router()


@router.message(Command("initgroup"))
async def init_group(message: Message):

    chat_id = message.chat.id

    async with await db() as conn:

        await conn.execute(
        "INSERT OR IGNORE INTO groups(chat_id,xp_step,max_level) VALUES(?,?,?)",
        (chat_id,100,25)
        )

        await conn.commit()

    await message.answer("Группа инициализирована")