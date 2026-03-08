from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class SetupStates(StatesGroup):
    waiting_levels = State()
    waiting_distance = State()
    waiting_names = State()

def settings_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Количество уровней", callback_data="set_levels")],
            [InlineKeyboardButton(text="📏 Дистанция XP", callback_data="set_distance")],
            [InlineKeyboardButton(text="🏷 Названия уровней", callback_data="set_names")]
        ]
    )

@router.message(Command("settings"))
async def open_settings(message: Message):
    await message.answer(
        "Настройки уровней",
        reply_markup=settings_keyboard()
    )

@router.callback_query(F.data == "set_levels")
async def ask_levels(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_levels)

    await call.message.answer(
        "Введите количество уровней (5-100)"
    )

@router.message(SetupStates.waiting_levels)
async def set_levels_value(message: Message, state: FSMContext):

    try:
        count = int(message.text)

        if count < 5 or count > 100:
            await message.answer("Можно от 5 до 100 уровней")
            return

        chat_id = message.chat.id

        set_level_count(chat_id, count)

        await message.answer(
            f"Установлено уровней: {count}",
            reply_markup=settings_keyboard()
        )

        await state.clear()

    except:
        await message.answer("Введите число")

@router.callback_query(F.data == "set_distance")
async def ask_distance(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_distance)

    await call.message.answer(
        "Введите дистанцию XP между уровнями"
    )

@router.message(SetupStates.waiting_distance)
async def set_distance(message: Message, state: FSMContext):

    try:
        xp = int(message.text)

        set_level_distance(message.chat.id, xp)

        await message.answer(
            f"Дистанция XP установлена: {xp}",
            reply_markup=settings_keyboard()
        )

        await state.clear()

    except:
        await message.answer("Введите число")

@router.callback_query(F.data == "set_names")
async def ask_names(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_names)

    await call.message.answer(
        "Введите названия уровней в формате:\n\n"
        "1. Новичок\n"
        "2. Боец\n"
        "3. Ветеран"
    )

@router.message(SetupStates.waiting_names)
async def set_names(message: Message, state: FSMContext):

    lines = message.text.split("\n")

    names = {}

    for line in lines:
        if "." in line:
            num, name = line.split(".", 1)
            try:
                lvl = int(num.strip())
                names[lvl] = name.strip()
            except:
                pass

    save_level_names(message.chat.id, names)

    await message.answer(
        "Названия уровней сохранены",
        reply_markup=settings_keyboard()
    )

    await state.clear()

@router.message(Command("setpic"))
async def set_picture(message: Message):

    await message.answer(
        "Отправьте изображение которое будет использоваться для карточки уровня"
    )

