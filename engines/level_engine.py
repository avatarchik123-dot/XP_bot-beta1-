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

    groups = load_json("groups.json")

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in groups:
        return

    user = groups[chat_id]["users"].get(user_id)

    if not user:
        return

    new_level = check_level(user["xp"])

    if new_level > user["level"]:
        user["level"] = new_level

        save_json("groups.json", groups)

        await message.answer(
            f"{message.from_user.first_name} достиг уровня {new_level}"
        )