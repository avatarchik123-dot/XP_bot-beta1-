from aiogram import Router
from aiogram.types import Message
from tinydb import Query

from services.database import db, get_level_names
from config import DEFAULT_XP_STEP, DEFAULT_MAX_LEVEL

router = Router()

users = db.table("users")
groups = db.table("groups")

User = Query()
Group = Query()


# антифлуд
last_message_time = {}

XP_PER_MESSAGE = 5
ANTI_FLOOD = 3


async def send_temp(message: Message, text: str):

    msg = await message.answer(text)

    try:
        await msg.delete()
    except:
        pass


@router.message()
async def handle_message(message: Message):

    if message.chat.type not in ["group", "supergroup"]:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    # ---------------- антифлуд ----------------

    import time

    now = time.time()

    key = f"{chat_id}_{user_id}"

    if key in last_message_time:

        if now - last_message_time[key] < ANTI_FLOOD:
            return

    last_message_time[key] = now

    # ---------------- пользователь ----------------

    user = users.get(
        (User.user_id == user_id) &
        (User.chat_id == chat_id)
    )

    if not user:

        users.insert({
            "user_id": user_id,
            "chat_id": chat_id,
            "xp": 0,
            "level": 1
        })

        user = users.get(
            (User.user_id == user_id) &
            (User.chat_id == chat_id)
        )

    # ---------------- настройки группы ----------------

    group = groups.get(Group.chat_id == chat_id)

    xp_step = DEFAULT_XP_STEP
    max_level = DEFAULT_MAX_LEVEL

    if group:

        if "distance" in group and group["distance"]:
            xp_step = group["distance"]

        if "levels" in group and group["levels"]:
            max_level = group["levels"]

    # ---------------- названия уровней ----------------

    level_names = get_level_names(chat_id)

    if not level_names:
        level_names = {}

    # ---------------- XP ----------------

    xp_gain = XP_PER_MESSAGE

    xp_total = user["xp"] + xp_gain
    old_level = user["level"]

    new_level = xp_total // xp_step + 1

    if new_level > max_level:
        new_level = max_level

    # ---------------- обновление базы ----------------

    users.update(
        {
            "xp": xp_total,
            "level": new_level
        },
        (User.user_id == user_id) &
        (User.chat_id == chat_id)
    )

    # ---------------- повышение уровня ----------------

    if new_level > old_level:

        level_name = level_names.get(new_level)

        if level_name:
            text = f"🎉 Новый уровень {new_level} — {level_name}"
        else:
            text = f"🎉 Новый уровень {new_level}"

        await send_temp(message, text)