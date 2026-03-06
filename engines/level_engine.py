from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import json
import os

router = Router()

DATA_PATH = "data/levels.json"


def load_levels():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump({}, f)

    with open(DATA_PATH, "r") as f:
        return json.load(f)


def save_levels(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_level(xp):
    level = 1
    need = 100
    while xp >= need:
        xp -= need
        level += 1
        need = int(need * 1.5)
    return level


@router.message()
async def handle_message(message: Message):

    if not message.text:
        return

    levels = load_levels()

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in levels:
        levels[chat_id] = {}

    if user_id not in levels[chat_id]:
        levels[chat_id][user_id] = {
            "xp": 0,
            "messages": 0
        }

    user = levels[chat_id][user_id]

    user["xp"] += 5
    user["messages"] += 1

    save_levels(levels)


@router.message(Command("rank"))
async def rank(message: Message):

    levels = load_levels()

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in levels or user_id not in levels[chat_id]:
        await message.reply("У тебя ещё нет XP.")
        return

    user = levels[chat_id][user_id]

    xp = user["xp"]
    messages = user["messages"]
    level = get_level(xp)

    text = (
        f"Твой уровень: {level}\n"
        f"XP: {xp}\n"
        f"Сообщений: {messages}"
    )

    await message.reply(text)




#*÷;#[×*]×;#;=['beo