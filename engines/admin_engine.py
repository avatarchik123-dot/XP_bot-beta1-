from aiogram import Router
from aiogram.types import Message

from services.file_manager import load_json, save_json

router = Router()


@router.message(lambda message: message.text == "/initgroup")
async def init_group(message: Message):

    if message.chat.type == "private":
        await message.answer("Эту команду нужно использовать в группе.")
        return

    group_id = str(message.chat.id)

    groups = load_json("groups.json")
    levels = load_json("levels.json")

    if group_id in groups:
        await message.answer("Группа уже инициализирована.")
        return

    groups[group_id] = {
        "title": message.chat.title
    }

    levels[group_id] = {}

    save_json("groups.json", groups)
    save_json("levels.json", levels)

    await message.answer("Группа успешно инициализирована.")