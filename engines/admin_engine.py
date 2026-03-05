from aiogram import Router
from aiogram.types import Message
from services.file_manager import load_json, save_json

router = Router()


@router.message(lambda m: m.text == "/initgroup")
async def init_group(message: Message):

    groups = load_json("groups.json")

    chat_id = str(message.chat.id)

    if chat_id not in groups:
        groups[chat_id] = {
            "users": {}
        }

        save_json("groups.json", groups)

        await message.answer("Группа инициализирована")

    else:
        await message.answer("Группа уже инициализирована")