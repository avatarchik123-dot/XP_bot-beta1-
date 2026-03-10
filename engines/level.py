from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import *
from engines.xp import text_xp
from services.database import users, groups, User, Group
from services.cache_manager import antiflood
from services.utils import send_temp

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

    await send_temp(message, f"Твой уровень: {level}\nXP: {xp}")


@router.message(Command("top"))
async def top_users(message: Message):

    chat_id = message.chat.id

    all_users = users.search(User.chat_id == chat_id)

    if not all_users:
        await send_temp(message, "Пока нет данных")
        return

    sorted_users = sorted(all_users, key=lambda x: x["xp"], reverse=True)[:5]

    text = "🏆 ТОП участников:\n\n"

    for i, u in enumerate(sorted_users, 1):
        text += f"{i}. {u['user_id']} — {u['xp']} XP\n"

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

    if not user:
        users.insert({
            "user_id": user_id,
            "chat_id": chat_id,
            "xp": xp,
            "level": 1
        })
        return

    xp_total = user["xp"] + xp
    old_level = user["level"]

    # Читаем настройки группы
    group = groups.get(Group.chat_id == chat_id)

    # Дефолтные значения
    xp_step = DEFAULT_XP_STEP
    max_level = DEFAULT_MAX_LEVEL
    level_names = {}

    # Если настройки есть — берём их
    if group:

        if "distance" in group and group["distance"]:
            xp_step = group["distance"]

        if "levels" in group and group["levels"]:
            max_level = group["levels"]

        if "names" in group and group["names"]:
            level_names = group["names"]

    # Рассчитываем уровень
    new_level = xp_total // xp_step + 1

    # Ограничение максимального уровня
    if new_level > max_level:
        new_level = max_level

    # Сначала обновляем базу
    users.update(
        {"xp": xp_total, "level": new_level},
        (User.user_id == user_id) & (User.chat_id == chat_id)
    )

    # Потом отправляем сообщение
    if new_level > old_level:

        level_name = None

        if level_names:
            level_name = level_names.get(str(new_level)) or level_names.get(new_level)

        if level_name:
            await send_temp(message, f"Новый уровень {new_level} — {level_name}")
        else:
            await send_temp(message, f"Новый уровень {new_level}")


async def auto_delete(msg):

    import asyncio

    await asyncio.sleep(AUTO_DELETE)

    try:
        await msg.delete()
    except:
        pass