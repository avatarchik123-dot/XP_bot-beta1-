from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.file_manager import load_json, save_json

router = Router()


@router.message(Command("initgroup"))
async def init_group(message: Message):

    if message.chat.type == "private":
        await message.answer("Эта команда работает только в группе.")
        return

    groups = load_json("groups.json")

    chat_id = str(message.chat.id)

    if chat_id not in groups:
        groups[chat_id] = {
            "name": message.chat.title,
            "users": {},
            "xp_enabled": True,
            "reactions_enabled": True,
            "levels": True
        }

        save_json("groups.json", groups)

        await message.answer("Группа успешно инициализирована.")
    else:
        await message.answer("Группа уже была инициализирована.")