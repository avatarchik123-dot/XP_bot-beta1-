from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.database import set_level_pic, get_level_pic
from services.utils import send_temp

router = Router()


# -------- проверка админа --------

async def is_admin(message: Message):

    member = await message.bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    return member.status in ["administrator", "creator"]


# -------- установка картинки уровня --------

@router.message(Command("setlevelpic"))
async def set_level_picture(message: Message):

    if not await is_admin(message):
        await send_temp(message, "Команда доступна только администраторам")
        return

    chat_id = message.chat.id

    args = message.text.split()

    if len(args) < 2:
        await send_temp(message, "Используй: /setlevelpic УРОВЕНЬ + фото или GIF")
        return

    try:
        level = int(args[1])
    except:
        await send_temp(message, "Уровень должен быть числом")
        return

    file_id = None

    if message.photo:
        file_id = message.photo[-1].file_id

    elif message.animation:
        file_id = message.animation.file_id

    elif message.document:
        file_id = message.document.file_id

    if not file_id:
        await send_temp(message, "Прикрепи фото или GIF вместе с командой")
        return

    set_level_pic(chat_id, level, file_id)

    await send_temp(message, f"Картинка для уровня {level} сохранена")


# -------- отправка картинки уровня --------

async def send_level_picture(message: Message, level: int, text: str):

    chat_id = message.chat.id

    file_id = get_level_pic(chat_id, level)

    # если картинки нет — обычный текст
    if not file_id:
        await send_temp(message, text)
        return

    try:

        await message.answer_animation(
            file_id,
            caption=text
        )

    except:

        await message.answer_photo(
            file_id,
            caption=text
        )