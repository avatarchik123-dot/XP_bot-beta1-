from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from config import *
from engines.xp import text_xp
from services.database import (
    users,
    User,
    get_settings,
    get_level_names,
    set_level_pic,
    get_level_pic,
    get_groups
)
from services.cache_manager import antiflood
from services.utils import send_temp

router = Router()

# ожидание картинки
waiting_picture = {}


# ===============================
# УСТАНОВКА КАРТИНКИ УРОВНЯ
# ===============================

@router.message(Command("setpic"))
async def set_level_pic_start(message: Message):

    if message.chat.type != "private":
        await message.answer("Команду нужно писать боту в личку")
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Используй: /setpic УРОВЕНЬ")
        return

    try:
        level = int(args[1])
    except:
        await message.answer("Уровень должен быть числом")
        return

    groups = get_groups()

    if not groups:
        await message.answer("Бот не добавлен ни в одну группу")
        return

    buttons = []

    for g in groups:

        title = g.get("title", str(g["chat_id"]))

        buttons.append([
            InlineKeyboardButton(
                text=title,
                callback_data=f"lvlpic_{g['chat_id']}_{level}"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        "Для какой группы установить картинку?",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("lvlpic_"))
async def choose_group(call: CallbackQuery):

    data = call.data.split("_")

    chat_id = int(data[1])
    level = int(data[2])

    waiting_picture[call.from_user.id] = {
        "chat_id": chat_id,
        "level": level
    }

    await call.message.answer(
        "Отправьте фото или GIF для этого уровня"
    )

    await call.answer()


@router.message()
async def receive_picture(message: Message):

    user_id = message.from_user.id

    if user_id not in waiting_picture:
        return

    data = waiting_picture[user_id]

    chat_id = data["chat_id"]
    level = data["level"]

    file_id = None

    if message.photo:
        file_id = message.photo[-1].file_id

    elif message.animation:
        file_id = message.animation.file_id

    elif message.document:
        file_id = message.document.file_id

    if not file_id:
        await message.answer("Нужно отправить фото или GIF")
        return

    set_level_pic(chat_id, level, file_id)

    del waiting_picture[user_id]

    await message.answer("✅ Изменения успешно сохранены")


async def send_level_picture(message: Message, level: int, text: str):

    chat_id = message.chat.id
    file_id = get_level_pic(chat_id, level)

    if not file_id:
        await message.answer(text)
        return

    try:
        await message.answer_photo(
            photo=file_id,
            caption=text
        )
        return
    except:
        pass

    try:
        await message.answer_animation(
            animation=file_id,
            caption=text
        )
        return
    except:
        pass

    await message.answer(text)


# ===============================
# КОМАНДЫ УРОВНЕЙ
# ===============================

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


# ===============================
# XP СИСТЕМА
# ===============================

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

    users.update(
        {
            "username": username,
            "first_name": first_name
        },
        (User.user_id == user_id) & (User.chat_id == chat_id)
    )

    xp_total = user["xp"] + xp
    old_level = user["level"]

    settings = get_settings(chat_id)

    xp_step = settings.get("distance") or DEFAULT_XP_STEP
    max_level = settings.get("levels") or DEFAULT_MAX_LEVEL

    level_names = get_level_names(chat_id)

    new_level = xp_total // xp_step + 1

    if new_level > max_level:
        new_level = max_level

    users.update(
        {"xp": xp_total, "level": new_level},
        (User.user_id == user_id) & (User.chat_id == chat_id)
    )

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

        await send_level_picture(message, new_level, text)