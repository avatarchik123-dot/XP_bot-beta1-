from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.database import groups, Group
from config import DEFAULT_XP_STEP, DEFAULT_MAX_LEVEL

router = Router()

@router.message(Command("initgroup"))
async def init_group(message: Message):

    chat_id = message.chat.id

    if groups.search(Group.chat_id == chat_id):
        await message.answer("Группа уже настроена")
        return

    groups.insert({
        "chat_id": chat_id,
        "xp_step": DEFAULT_XP_STEP,
        "max_level": DEFAULT_MAX_LEVEL
    })

    await message.answer("Группа инициализирована")