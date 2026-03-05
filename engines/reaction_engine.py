from aiogram import Router
from aiogram.types import MessageReactionUpdated

from services.file_manager import load_json, save_json

router = Router()


@router.message_reaction()
async def reaction_xp(event: MessageReactionUpdated):

    chat_id = str(event.chat.id)
    user_id = str(event.user.id)

    groups = load_json("groups.json")

    if chat_id not in groups:
        return

    users = groups[chat_id]["users"]

    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "level": 1
        }

    users[user_id]["xp"] += 1

    save_json("groups.json", groups)