from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

@router.message(Command("settings"))
async def open_settings(message: Message):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
        ]
    )

    await message.answer("Меню настроек", reply_markup=kb)