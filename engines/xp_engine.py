from aiogram import Router, F
from aiogram.types import Message
import time
from services.file_manager import load_json, save_json

router = Router()

ANTI_FLOOD = 3

last_message_time = {}

def calculate_text_xp(text: str):
    length = len(text)

    if length < 3:
        return 0
    if 3 <= length <= 9:
        return 1
    if 10 <= length <= 29:
        return 2
    if 30 <= length <= 49:
        return 3
    if length >= 50:
        return 5

    return 0


@router.message(F.chat.type.in_(["group", "supergroup"]))
async def handle_message(message: Message):

    if message.from_user.is_bot:
        return

    user_id = str(message.from_user.id)
    group_id = str(message.chat.id)

    now = time.time()

    if user_id in last_message_time:
        if now - last_message_time[user_id] < ANTI_FLOOD:
            return

    last_message_time[user_id] = now

    xp = 0

    if message.text:
        xp += calculate_text_xp(message.text)

    if message.photo:
        xp += 3

    if message.video:
        xp += 5

    if xp == 0:
        return

    data = load_json("data/levels.json")

    if group_id not in data:
        data[group_id] = {}

    if user_id not in data[group_id]:
        data[group_id][user_id] = {
            "xp": 0,
            "level": 0
        }

    data[group_id][user_id]["xp"] += xp

    save_json("data/levels.json", data)