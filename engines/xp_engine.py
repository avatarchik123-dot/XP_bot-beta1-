import time
from aiogram import Router
from aiogram.types import Message

from services.file_manager import load_json, save_json

router = Router()

cooldowns = {}


@router.message()
async def give_xp(message: Message):

    if message.chat.type == "private":
        return

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)

    now = time.time()

    if user_id in cooldowns:
        if now - cooldowns[user_id] < 3:
            return

    cooldowns[user_id] = now

    groups = load_json("groups.json")

    if chat_id not in groups:
        return

    users = groups[chat_id]["users"]

    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "level": 1
        }

    xp_gain = min(len(message.text or ""), 25)

    users[user_id]["xp"] += xp_gain

    save_json("groups.json", groups)