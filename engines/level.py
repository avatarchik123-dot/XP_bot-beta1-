from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import *
from engines.xp import text_xp
from services.database import (
    users,
    User,
    get_settings,
    get_level_names
)
from services.cache_manager import antiflood
from services.utils import send_temp
from services.pic import send_level_picture

router = Router()


@router.message(Command("rank"))
async def rank(message: Message):

    user_id = message.from_user.id
    chat_id = message.chat.id

    user = users.get((User.user_id == user_id) & (User.chat_id == chat_id))

    if not user:
        await send_temp(message, "У тебя пока нет XP")
        return

    xp = user["xp"]
    level = user["level"]

    level_names = get_level_names(chat_id)
    level_name = level_names.get(level)

    if level_name:
        text = (
            f'Звание: "{level_name}"\n'
            f'Твой уровень: {level}\n'
            f'XP: {xp}'
        )
    else:
        text = (
            f'Твой уровень: {level}\n'
            f'XP: {xp}'
        )

    await send_temp(message, text)


@router.message(Command("top"))
async def top_users(message: Message):

    chat_id = message.chat.id

    all_users = users.search(User.chat_id == chat_id)

    if not all_users:
        await send_temp(message, "Пока нет данных")
        return

    sorted_users = sorted(all_users, key=lambda x: x["xp"], reverse=True)[:10]

    text = "🏆 ТОП участников:\n\n"

    for i, u in enumerate(sorted_users, 1):

        username = u.get("username")
        first_name = u.get("first_name")

        if username:
            name = f"@{username}"
        elif first_name:
            name = first_name
        else:
            name = str(u["user_id"])

        text += f"{i}. {name} — {u['xp']} XP\n"

    await send_temp(message, text)


@router.message()
async def handle_message(message: Message):

    if message.chat.type == "private":
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    if not antiflood(user_id, ANTIFLOOD):
        return

    xp = 0

    if message.text:
        xp += text_xp(message.text)

    if message.photo:
        xp += XP_PHOTO

    if message.sticker:
        xp += XP_STICKER

    if message.video:
        xp += XP_VIDEO

    if message.audio:
        xp += XP_AUDIO

    if xp == 0:
        return

    user = users.get((User.user_id == user_id) & (User.chat_id == chat_id))

    username = message.from_user.username
    first_name = message.from_user.first_name

    if not user:
        users.insert({
            "user_id": user_id,
            "chat_id": chat_id,
            "xp": xp,
            "level": 1,
            "username": username,
            "first_name": first_name
        })
        return

    # обновляем имя если изменилось
    users.update(
        {
            "username": username,
            "first_name": first_name
        },
        (User.user_id == user_id) & (User.chat_id == chat_id)
    )

    xp_total = user["xp"] + xp
    old_level = user["level"]

    # ---------- настройки ----------

    settings = get_settings(chat_id)

    xp_step = settings.get("distance") or DEFAULT_XP_STEP
    max_level = settings.get("levels") or DEFAULT_MAX_LEVEL

    # ---------- названия уровней ----------

    level_names = get_level_names(chat_id)

    # ---------- расчет уровня ----------

    new_level = xp_total // xp_step + 1

    if new_level > max_level:
        new_level = max_level

    # ---------- обновление базы ----------

    users.update(
        {"xp": xp_total, "level": new_level},
        (User.user_id == user_id) & (User.chat_id == chat_id)
    )

    # ---------- сообщение о новом уровне ----------

    if new_level > old_level:

        level_name = level_names.get(new_level)

        if username:
            user_tag = f"@{username}"
        else:
            user_tag = first_name

        if level_name:
            text = (
                f'Поздравляем {user_tag} '
                f'с достижением нового уровня "{new_level}" - "{level_name}"'
            )
        else:
            text = (
                f'Поздравляем {user_tag} '
                f'с достижением нового уровня "{new_level}"'
            )

        await send_temp(message, text)


async def auto_delete(msg):

    import asyncio

    await asyncio.sleep(AUTO_DELETE)

    try:
        await msg.delete()
    except:
        pass