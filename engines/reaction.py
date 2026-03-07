from aiogram import Router
from aiogram.types import MessageReactionUpdated

from config import XP_REACTION, MAX_REACTIONS
from services.database import reactions, users, Reaction, User

router = Router()

@router.message_reaction()
async def reaction_handler(event: MessageReactionUpdated):

    reactor = event.user.id
    message_id = event.message_id
    chat_id = event.chat.id

    key = f"{message_id}_{reactor}"

    if reactions.get(Reaction.key == key):
        return

    reactions.insert({
        "key": key,
        "message_id": message_id,
        "reactor": reactor
    })