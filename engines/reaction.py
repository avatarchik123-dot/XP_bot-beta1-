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
        "key": key
    })

    message_author = event.actor_chat

    if not message_author:
        return

    author_id = message_author.id

    user = users.get((User.user_id == author_id) & (User.chat_id == chat_id))

    if not user:
        return

    xp_total = user["xp"] + XP_REACTION

    users.update(
        {"xp": xp_total},
        (User.user_id == author_id) & (User.chat_id == chat_id)
    )