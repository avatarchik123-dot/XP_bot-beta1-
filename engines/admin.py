from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.utils import send_temp
from services.database import groups, Group
from config import DEFAULT_XP_STEP, DEFAULT_MAX_LEVEL
from services.database import add_xp, remove_xp

router = Router()


async def is_admin(message: Message):

    member = await message.bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    return member.status in ["administrator", "creator"]


@router.message(Command("help"))
async def help_cmd(message: Message):

    text = (
        "Команды бота:\n\n"
        "/rank — твой уровень\n"
        "/top — топ участников\n"
        "/initgroup — инициализация группы\n"
    )

    await send_temp(message, text)


@router.message(Command("initgroup"))
async def init_group(message: Message):

    if not await is_admin(message):
        return

    chat_id = message.chat.id

    if groups.search(Group.chat_id == chat_id):
        await send_temp(message, "Группа уже настроена")
        return

    groups.insert({
        "chat_id": chat_id,
        "xp_step": DEFAULT_XP_STEP,
        "max_level": DEFAULT_MAX_LEVEL
    })

    await send_temp(message, "Группа инициализирована")


@router.message(Command("addxp"))
async def add_xp_cmd(message: Message):

    if not await is_admin(message):
        return

    if not message.reply_to_message:
        await send_temp(message, "Используй команду ответом на сообщение\n\n/addxp 50")
        return

    args = message.text.split()

    if len(args) < 2:
        await send_temp(message, "Пример:\n/addxp 50")
        return

    if not args[1].isdigit():
        await send_temp(message, "XP должно быть числом")
        return

    xp = int(args[1])

    if xp < 1 or xp > 500:
        await send_temp(message, "XP должно быть от 1 до 500")
        return

    user = message.reply_to_message.from_user

    new_xp = add_xp(
        message.chat.id,
        user.id,
        xp
    )

    await send_temp(
        message,
        f"{user.full_name} получил {xp} XP\nТеперь: {new_xp}"
    )


@router.message(Command("removexp"))
async def remove_xp_cmd(message: Message):

    if not await is_admin(message):
        return

    if not message.reply_to_message:
        await send_temp(message, "Используй команду ответом на сообщение\n\n/removexp 50")
        return

    args = message.text.split()

    if len(args) < 2:
        await send_temp(message, "Пример:\n/removexp 50")
        return

    if not args[1].isdigit():
        await send_temp(message, "XP должно быть числом")
        return

    xp = int(args[1])

    if xp < 1 or xp > 500:
        await send_temp(message, "XP должно быть от 1 до 500")
        return

    user = message.reply_to_message.from_user

    new_xp = remove_xp(
        message.chat.id,
        user.id,
        xp
    )

    await send_temp(
        message,
        f"У {user.full_name} снято {xp} XP\nТеперь: {new_xp}"
    )