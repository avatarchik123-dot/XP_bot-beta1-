from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.utils import send_temp
from services.database import groups, Group
from config import DEFAULT_XP_STEP, DEFAULT_MAX_LEVEL
from services.database import add_xp, remove_xp

router = Router()

@router.message(Command("help"))
async def help_cmd(message: Message):

    text = (
        "Команды бота:\n\n"
        "/rank — твой уровень\n"
        "/top — топ участников\n"
        "/initgroup — инициализация группы\n"
    )

    await send_temp(message,text)

@router.message(Command("initgroup"))
async def init_group(message: Message):

    chat_id = message.chat.id

    if groups.search(Group.chat_id == chat_id):
        await send_temp(message,"Группа уже настроена")
        return

    groups.insert({
        "chat_id": chat_id,
        "xp_step": DEFAULT_XP_STEP,
        "max_level": DEFAULT_MAX_LEVEL
    })

    await send_temp(message,"Группа инициализирована")

@router.message(Command("addxp"))
async def add_xp_cmd(message: Message):

    args = message.text.split()

    if len(args) < 3 or not message.entities:
        await send_temp(message,"Пример:\n/addxp @user 50")
        return

    if not args[2].isdigit():
        await send_temp(message,"XP должно быть числом")
        return

    xp = int(args[2])

    if xp < 1 or xp > 500:
        await send_temp(message,"XP должно быть 1-500")
        return

    user = message.entities[0].user

    new_xp = add_xp(
        message.chat.id,
        user.id,
        xp
    )

    await send_temp(
        message,
        f"Добавлено {xp} XP\nТеперь: {new_xp}"
    )

@router.message(Command("removexp"))
async def remove_xp_cmd(message: Message):

    args = message.text.split()

    if len(args) < 3 or not message.entities:
        await send_temp(message,"Пример:\n/removexp @user 50")
        return

    if not args[2].isdigit():
        await send_temp(message,"XP должно быть числом")
        return

    xp = int(args[2])

    if xp < 1 or xp > 500:
        await send_temp(message,"XP должно быть 1-500")
        return

    user = message.entities[0].user

    new_xp = remove_xp(
        message.chat.id,
        user.id,
        xp
    )

    await send_temp(
        message,
        f"Снято {xp} XP\nТеперь: {new_xp}"
    )