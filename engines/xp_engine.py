from aiogram import Router
from aiogram.types import Message

from services.file_manager import load_json, save_json

router = Router()


@router.message()
async def xp_from_message(message: Message):

    if message.chat.type == "private":
        return

    group_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    groups = load_json("groups.json")

    if group_id not in groups:
        return

    levels = load_json("levels.json")

    if group_id not in levels:
        levels[group_id] = {}

    if user_id not in levels[group_id]:
        levels[group_id][user_id] = {
            "xp": 0,
            "level": 1
        }

    xp_gain = max(1, len(message.text or "") // 5)

    levels[group_id][user_id]["xp"] += xp_gain

    save_json("levels.json", levels)