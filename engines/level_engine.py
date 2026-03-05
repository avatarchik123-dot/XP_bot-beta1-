from aiogram import Router
from aiogram.types import Message

from services.file_manager import load_json, save_json

router = Router()


@router.message()
async def level_system(message: Message):

    if not message.chat:
        return

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    groups = load_json("data/groups.json")

    if chat_id not in groups:
        return

    if "users" not in groups[chat_id]:
        groups[chat_id]["users"] = {}

    users = groups[chat_id]["users"]

    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "level": 1
        }

    users[user_id]["xp"] += 5

    save_json("data/groups.json", groups)