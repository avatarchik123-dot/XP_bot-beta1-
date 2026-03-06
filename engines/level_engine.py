from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.file_manager import load_json, save_json

router = Router()

XP_PER_MESSAGE = 5


@router.message()
async def add_xp(message: Message):

    if message.chat.type == "private":
        return

    groups = load_json("data/groups.json")

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in groups:
        return

    if "users" not in groups[chat_id]:
        groups[chat_id]["users"] = {}

    users = groups[chat_id]["users"]

    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "level": 1
        }

    users[user_id]["xp"] += XP_PER_MESSAGE

    save_json("data/groups.json", groups)


@router.message(Command("rank"))
async def rank(message: Message):

    groups = load_json("data/groups.json")

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in groups:
        await message.reply("Группа не инициализирована.")
        return

    users = groups[chat_id].get("users", {})

    if user_id not in users:
        await message.reply("У тебя пока 0 XP.")
        return

    xp = users[user_id]["xp"]
    level = users[user_id]["level"]

    await message.reply(
        f"Твой уровень: {level}\n"
        f"XP: {xp}"
    )