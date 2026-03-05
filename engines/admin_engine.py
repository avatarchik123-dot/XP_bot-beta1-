from aiogram import Router
from aiogram.types import Message
from services.file_manager import load_json, save_json

router = Router()


def is_admin(member):
    return member.status in ["administrator", "creator"]


@router.message(commands=["initgroup"])
async def init_group(message: Message):

    chat = message.chat
    user = message.from_user

    member = await message.bot.get_chat_member(chat.id, user.id)

    if not is_admin(member):
        await message.reply("Только администратор может выполнить эту команду.")
        return

    groups = load_json("data/groups.json")

    groups[str(chat.id)] = {
        "title": chat.title
    }

    save_json("data/groups.json", groups)

    await message.reply("Группа инициализирована.")


@router.message(commands=["addxp"])
async def add_xp(message: Message):

    chat = message.chat
    user = message.from_user

    member = await message.bot.get_chat_member(chat.id, user.id)

    if not is_admin(member):
        return

    if not message.reply_to_message:
        await message.reply("Ответьте на сообщение пользователя.")
        return

    args = message.text.split()

    if len(args) < 2:
        return

    amount = int(args[1])

    target = message.reply_to_message.from_user.id

    data = load_json("data/levels.json")

    group_id = str(chat.id)
    user_id = str(target)

    if group_id not in data:
        data[group_id] = {}

    if user_id not in data[group_id]:
        data[group_id][user_id] = {"xp": 0, "level": 0}

    data[group_id][user_id]["xp"] += amount

    save_json("data/levels.json", data)

    await message.reply(f"Добавлено {amount} XP")


@router.message(commands=["removexp"])
async def remove_xp(message: Message):

    chat = message.chat
    user = message.from_user

    member = await message.bot.get_chat_member(chat.id, user.id)

    if not is_admin(member):
        return

    if not message.reply_to_message:
        await message.reply("Ответьте на сообщение пользователя.")
        return

    args = message.text.split()

    if len(args) < 2:
        return

    amount = int(args[1])

    target = message.reply_to_message.from_user.id

    data = load_json("data/levels.json")

    group_id = str(chat.id)
    user_id = str(target)

    if group_id not in data:
        return

    if user_id not in data[group_id]:
        return

    data[group_id][user_id]["xp"] -= amount

    save_json("data/levels.json", data)

    await message.reply(f"Убрано {amount} XP")