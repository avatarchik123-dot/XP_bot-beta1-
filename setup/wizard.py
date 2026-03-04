from aiogram import types
from aiogram.filters import Command

def register_wizard_handlers(dp):

    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.answer(
            "➕ Добавить в группу\n"
            "⚙️ Настроить бота\n"
            "📂 Мои группы"
        )