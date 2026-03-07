from aiogram import Router
from aiogram.types import MessageReactionUpdated

from config import XP_REACTION
from services.database import reactions, users, Reaction, User

router = Router()


@router.message_reaction()
async def reaction_handler(event: MessageReactionUpdated, bot):

    reactor = event.user.id
    message_id = event.message_id
    chat_id = event.chat.id

    key = f"{message_id}_{reactor}"

    if reactions.get(Reaction.key == key):
        return

    reactions.insert({
        "key": key
    })

    message = await bot.get_message(chat_id, message_id)

    if not message.from_user:
        return

    author_id = message.from_user.id

    user = users.get((User.user_id == author_id) & (User.chat_id == chat_id))

    if not user:
        return

    xp_total = user["xp"] + XP_REACTION

    users.update(
        {"xp": xp_total},
        (User.user_id == author_id) & (User.chat_id == chat_id)
    )