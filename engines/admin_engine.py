from aiogram import Router

router = Router()

from aiogram import types
from aiogram.filters import Command
from services.file_manager import load, save
from services.cache_manager import get, set, invalidate

def register_admin_handlers(dp):

    @dp.message(Command("initgroup"))
    async def init_group(message: types.Message):
        group_id = str(message.chat.id)

        groups = load("groups.json")

        if group_id not in groups:
            groups[group_id] = {
                "users": {},
                "logs": []
            }

        save("groups.json", groups)
        await message.answer("Группа инициализирована.")

    @dp.message(Command("top"))
    async def top(message: types.Message):
        group_id = str(message.chat.id)

        cached = get(f"top_{group_id}")
        if cached:
            await message.answer(cached)
            return

        groups = load("groups.json")
        users = groups[group_id]["users"]

        sorted_users = sorted(users.items(), key=lambda x: x[1]["xp"], reverse=True)[:5]

        text = "🏆 Топ 5:\n\n"
        for i, (uid, data) in enumerate(sorted_users, 1):
            text += f"{i}. {uid} — {data['xp']} XP\n"

        set(f"top_{group_id}", text)
        await message.answer(text)