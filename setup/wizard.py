from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


# ---------------- СОСТОЯНИЯ ----------------

class SetupStates(StatesGroup):
    waiting_levels = State()
    waiting_distance = State()
    waiting_names = State()


# ---------------- КЛАВИАТУРА ----------------

def settings_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Количество уровней", callback_data="set_levels")],
            [InlineKeyboardButton(text="📏 Дистанция XP", callback_data="set_distance")],
            [InlineKeyboardButton(text="🏷 Названия уровней", callback_data="set_names")]
        ]
    )


# ---------------- ОТКРЫТИЕ МЕНЮ ----------------

@router.message(Command("settings"))
async def open_settings(message: Message):

    await message.answer(
        "⚙️ Настройки уровней",
        reply_markup=settings_keyboard()
    )


# ---------------- КНОПКА КОЛИЧЕСТВА УРОВНЕЙ ----------------

@router.callback_query(F.data == "set_levels")
async def ask_levels(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_levels)

    await call.message.answer(
        "Введите количество уровней (5-100)"
    )


# ---------------- СОХРАНЕНИЕ КОЛИЧЕСТВА ----------------

@router.message(SetupStates.waiting_levels)
async def set_levels_value(message: Message, state: FSMContext):

    try:
        count = int(message.text)

        if count < 5 or count > 100:
            await message.answer("Можно установить от 5 до 100 уровней")
            return

        chat_id = message.chat.id

        # твоя функция сохранения
        set_level_count(chat_id, count)

        await message.answer(
            f"✅ Установлено уровней: {count}",
            reply_markup=settings_keyboard()
        )

        await state.clear()

    except:
        await message.answer("Введите число")


# ---------------- ДИСТАНЦИЯ XP ----------------

@router.callback_query(F.data == "set_distance")
async def ask_distance(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_distance)

    await call.message.answer(
        "Введите дистанцию XP между уровнями"
    )


# ---------------- СОХРАНЕНИЕ ДИСТАНЦИИ ----------------

@router.message(SetupStates.waiting_distance)
async def set_distance(message: Message, state: FSMContext):

    try:
        xp = int(message.text)

        chat_id = message.chat.id

        # твоя функция
        set_level_distance(chat_id, xp)

        await message.answer(
            f"✅ Дистанция XP установлена: {xp}",
            reply_markup=settings_keyboard()
        )

        await state.clear()

    except:
        await message.answer("Введите число")


# ---------------- НАЗВАНИЯ УРОВНЕЙ ----------------

@router.callback_query(F.data == "set_names")
async def ask_names(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_names)

    await call.message.answer(
        "Введите названия уровней в формате:\n\n"
        "1. Новичок\n"
        "2. Актив\n"
        "3. Флудер\n"
        "4. Легенда"
    )


# ---------------- СОХРАНЕНИЕ НАЗВАНИЙ ----------------

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

    chat_id = message.chat.id

    # твоя функция
    save_level_names(chat_id, names)

    await message.answer(
        "✅ Названия уровней сохранены",
        reply_markup=settings_keyboard()
    )

    await state.clear()


# ---------------- КОМАНДА УСТАНОВКИ КАРТИНКИ ----------------

@router.message(Command("setpic"))
async def set_pic(message: Message):

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование: /setpic номер_уровня")
        return

    level = args[1]

    await message.answer(
        f"Отправьте картинку или gif для уровня {level}"
    )