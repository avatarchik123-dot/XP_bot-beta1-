from aiogram import Router
from aiogram.types import Message
from services.file_manager import load_json

router = Router()


def get_level(xp):
    return xp // 100


@router.message(commands=["rank"])
async def rank(message: Message):

    group_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    data = load_json("data/levels.json")

    if group_id not in data:
        await message.reply("Нет данных.")
        return

    if user_id not in data[group_id]:
        await message.reply("У вас пока нет XP.")
        return

    xp = data[group_id][user_id]["xp"]
    level = get_level(xp)

    next_level = (level + 1) * 100
    remain = next_level - xp

    bar = int((xp % 100) / 10)

    progress = "█" * bar + "░" * (10 - bar)

    text = (
        f"Уровень: {level}\n"
        f"XP: {xp}\n"
        f"До следующего: {remain}\n"
        f"[{progress}]"
    )

    await message.reply(text)


@router.message(commands=["top"])
async def top(message: Message):

    group_id = str(message.chat.id)

    data = load_json("data/levels.json")

    if group_id not in data:
        await message.reply("Нет данных.")
        return

    users = data[group_id]

    sorted_users = sorted(
        users.items(),
        key=lambda x: x[1]["xp"],
        reverse=True
    )[:5]

    text = "🏆 Топ 5\n\n"

    for i, (user_id, info) in enumerate(sorted_users, start=1):
        xp = info["xp"]
        level = xp // 100

        text += f"{i}. {user_id} | lvl {level} | {xp} XP\n"

    await message.reply(text)