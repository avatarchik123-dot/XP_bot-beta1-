from aiogram import Router
from aiogram.types import MessageReactionUpdated
from services.file_manager import load_json, save_json

router = Router()

MAX_REACTION_XP = 50

reaction_counter = {}


@router.message_reaction()
async def reaction_handler(event: MessageReactionUpdated):

    group_id = str(event.chat.id)
    message_id = event.message_id

    key = f"{group_id}:{message_id}"

    if key not in reaction_counter:
        reaction_counter[key] = 0

    if reaction_counter[key] >= MAX_REACTION_XP:
        return

    user_id = str(event.user.id)

    data = load_json("data/levels.json")

    if group_id not in data:
        return

    if user_id not in data[group_id]:
        data[group_id][user_id] = {
            "xp": 0,
            "level": 0
        }

    data[group_id][user_id]["xp"] += 1

    reaction_counter[key] += 1

    save_json("data/levels.json", data)