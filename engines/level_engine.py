from aiogram import Router
from aiogram.types import Message

from services.file_manager import load_json, save_json

router = Router()


def check_level(xp):

    level = 1

    while xp >= level * 100:
        level += 1

    return level


@router.message()
async def level_system(message: Message):

    if message.chat.type == "private":
    return

groups = load_json("data/groups.json")

if str(chat_id) not in groups:
return

if "users" not in groups[str(chat_id)]:
    groups[str(chat_id)]["users"] = {}

user = groups[str(chat_id)]["users"].get(str(user_id))

if not user:
    groups[str(chat_id)]["users"][str(user_id)] = {
        "xp": 0,
        "level": 1
    }
    user = groups[str(chat_id)]["users"][str(user_id)]

user["xp"] += 5

save_json("data/groups.json", groups)
await message.answer(
            f"{message.from_user.first_name} достиг уровня {new_level}"
        )