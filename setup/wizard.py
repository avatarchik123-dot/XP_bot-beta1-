from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.message(Command("settings"))
async def open_settings(message: Message):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
        ]
    )

    await message.answer("Меню настроек", reply_markup=kb)


@router.callback_query(F.data == "settings")
async def settings_menu(call: CallbackQuery):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Количество уровней", callback_data="set_levels")],
            [InlineKeyboardButton(text="📏 Дистанция XP", callback_data="set_distance")],
            [InlineKeyboardButton(text="🏷 Названия уровней", callback_data="set_names")]
        ]
    )

    await call.message.edit_text("Настройки уровней", reply_markup=kb)


@router.callback_query(F.data == "set_levels")
async def ask_levels(call: CallbackQuery):

    await call.message.answer("Введите количество уровней (5-100)")