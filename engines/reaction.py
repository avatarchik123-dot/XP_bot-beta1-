from aiogram import Router
from aiogram.types import MessageReactionUpdated

from config import XP_REACTION
from services.file_manager import db

router = Router()


@router.message_reaction()
async def reaction_handler(event: MessageReactionUpdated):

    reactor = event.user.id
    message_id = event.message_id
    chat_id = event.chat.id

    async with await db() as conn:

        cur = await conn.execute(
        "SELECT reactor_id FROM reactions WHERE message_id=? AND reactor_id=?",
        (message_id,reactor)
        )

        if await cur.fetchone():
            return

        await conn.execute(
        "INSERT INTO reactions(message_id,reactor_id) VALUES(?,?)",
        (message_id,reactor)
        )

        await conn.commit()