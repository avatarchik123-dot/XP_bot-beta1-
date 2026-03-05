from aiogram import Router

router = Router()

import time
from aiogram import types
from services.file_manager import load, save
from services.cache_manager import invalidate

user_cooldown = {}
user_last_messages = {}

def calculate_text_xp(text):
    length = len(text)
    if length < 3:
        return 0
    if 3 <= length <= 9:
        return 1
    if 10 <= length <= 29:
        return 2
    if 30 <= length <= 49:
        return 3
    return 5

def register_xp_handlers(dp):

    @dp.message()
    async def handle_message(message: types.Message):
        if not message.text and not message.photo and not message.video:
            return

        if message.from_user.is_bot:
            return

        if message.text and message.text.startswith("/"):
            return

        user_id = str(message.from_user.id)
        group_id = str(message.chat.id)

        now = time.time()

        if user_id in user_cooldown:
            if now - user_cooldown[user_id] < 3:
                return

        user_cooldown[user_id] = now

        if user_id not in user_last_messages:
            user_last_messages[user_id] = []

        last_msgs = user_last_messages[user_id]

        if message.text:
            if last_msgs.count(message.text) >= 2:
                return
            last_msgs.append(message.text)
            if len(last_msgs) > 3:
                last_msgs.pop(0)

        xp = 0

        if message.text:
            xp += calculate_text_xp(message.text)

        if message.photo:
            xp += 3
        if message.video:
            xp += 5

        if xp == 0:
            return

        groups = load("groups.json")
        if group_id not in groups:
            return

        if user_id not in groups[group_id]["users"]:
            groups[group_id]["users"][user_id] = {
                "xp": 0,
                "level": 0
            }

        groups[group_id]["users"][user_id]["xp"] += xp

        save("groups.json", groups)
        invalidate(f"top_{group_id}")