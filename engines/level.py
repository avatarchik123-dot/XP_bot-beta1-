from aiogram import Router
from aiogram.types import Message

from engines.xp import calc_xp_text
from services.cache_manager import check_antiflood
from services.file_manager import db

router = Router()


@router.message()
async def level_system(message: Message):

    if message.chat.type == "private":
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    if not check_antiflood(user_id):
        return

    text = message.text or ""

    xp = calc_xp_text(len(text))

    async with await db() as conn:

        cur = await conn.execute(
        "SELECT xp,level FROM users WHERE user_id=? AND chat_id=?",
        (user_id,chat_id)
        )

        user = await cur.fetchone()

        if not user:

            await conn.execute(
            "INSERT INTO users(user_id,chat_id,xp,level) VALUES(?,?,?,?)",
            (user_id,chat_id,xp,1)
            )

        else:

            xp_total = user[0] + xp

            level = user[1]

            cur = await conn.execute(
            "SELECT xp_step FROM groups WHERE chat_id=?",
            (chat_id,)
            )

            xp_step = (await cur.fetchone())[0]

            if xp_total >= level * xp_step:

                level += 1

                await message.answer(f"Новый уровень {level}")

            await conn.execute(
            "UPDATE users SET xp=?,level=? WHERE user_id=? AND chat_id=?",
            (xp_total,level,user_id,chat_id)
            )

        await conn.commit()