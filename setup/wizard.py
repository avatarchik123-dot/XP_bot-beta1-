import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

DATA_FILE = "data/levels.json"


# ---------------- БАЗА ----------------

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- СОСТОЯНИЯ ----------------

class SetupStates(StatesGroup):

    choosing_group = State()

    waiting_levels = State()
    confirm_levels = State()

    waiting_distance = State()
    confirm_distance = State()

    waiting_names = State()
    confirm_names = State()


# ---------------- КЛАВИАТУРЫ ----------------

def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Количество уровней", callback_data="set_levels")],
            [InlineKeyboardButton(text="📏 Дистанция XP", callback_data="set_distance")],
            [InlineKeyboardButton(text="🏷 Названия уровней", callback_data="set_names")],
            [InlineKeyboardButton(text="📋 Текущие параметры", callback_data="current")]
        ]
    )


def confirm_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )


# ---------------- START ----------------

@router.message(Command("settings"))
async def settings_start(message: Message, state: FSMContext):

    await state.set_state(SetupStates.choosing_group)

    await message.answer(
        "Отправьте ID группы для настройки"
    )


# ---------------- ВЫБОР ГРУППЫ ----------------

@router.message(SetupStates.choosing_group)
async def set_group(message: Message, state: FSMContext):

    try:

        group_id = int(message.text)

        await state.update_data(group=group_id)

        await message.answer(
            f"Группа выбрана: {group_id}",
            reply_markup=main_menu()
        )

        await state.clear()

    except:
        await message.answer("Введите корректный ID группы")


# ---------------- КОЛИЧЕСТВО УРОВНЕЙ ----------------

@router.callback_query(F.data == "set_levels")
async def ask_levels(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_levels)

    await call.message.answer(
        "Укажите количество уровней (5-100)"
    )


@router.message(SetupStates.waiting_levels)
async def receive_levels(message: Message, state: FSMContext):

    try:

        value = int(message.text)

        if value < 5 or value > 100:
            await message.answer("Допустимо 5-100")
            return

        await state.update_data(temp_levels=value)

        await state.set_state(SetupStates.confirm_levels)

        await message.answer(
            f"Установить {value} уровней?",
            reply_markup=confirm_menu()
        )

    except:
        await message.answer("Введите число")


# ---------------- ДИСТАНЦИЯ XP ----------------

@router.callback_query(F.data == "set_distance")
async def ask_distance(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_distance)

    await call.message.answer(
        "Введите дистанцию XP между уровнями"
    )


@router.message(SetupStates.waiting_distance)
async def receive_distance(message: Message, state: FSMContext):

    try:

        value = int(message.text)

        await state.update_data(temp_distance=value)

        await state.set_state(SetupStates.confirm_distance)

        await message.answer(
            f"Установить дистанцию {value} XP?",
            reply_markup=confirm_menu()
        )

    except:
        await message.answer("Введите число")


# ---------------- НАЗВАНИЯ УРОВНЕЙ ----------------

@router.callback_query(F.data == "set_names")
async def ask_names(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_names)

    await call.message.answer(
        "Введите названия уровней\n\n"
        "1. Новичок\n"
        "2. Актив\n"
        "3. Флудер"
    )


@router.message(SetupStates.waiting_names)
async def receive_names(message: Message, state: FSMContext):

    lines = message.text.split("\n")

    names = {}

    for line in lines:

        if "." in line:

            num, name = line.split(".", 1)

            try:
                names[int(num)] = name.strip()
            except:
                pass

    await state.update_data(temp_names=names)

    await state.set_state(SetupStates.confirm_names)

    await message.answer(
        "Сохранить названия уровней?",
        reply_markup=confirm_menu()
    )


# ---------------- ПОДТВЕРЖДЕНИЕ ----------------

@router.callback_query(F.data == "confirm")
async def confirm(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    db = load_data()

    group = str(data["group"])

    if group not in db:
        db[group] = {}

    if "temp_levels" in data:
        db[group]["levels"] = data["temp_levels"]

    if "temp_distance" in data:
        db[group]["distance"] = data["temp_distance"]

    if "temp_names" in data:
        db[group]["names"] = data["temp_names"]

    save_data(db)

    await call.message.answer(
        "Настройки сохранены",
        reply_markup=main_menu()
    )

    await state.clear()


# ---------------- ОТМЕНА ----------------

@router.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery, state: FSMContext):

    await call.message.answer(
        "Действие отменено",
        reply_markup=main_menu()
    )

    await state.clear()


# ---------------- ТЕКУЩИЕ ПАРАМЕТРЫ ----------------

@router.callback_query(F.data == "current")
async def current(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    group = str(data.get("group"))

    db = load_data()

    if group not in db:

        await call.message.answer("Настройки ещё не заданы")
        return

    g = db[group]

    names = ""

    if "names" in g:

        for lvl, name in g["names"].items():
            names += f"{lvl}. {name}\n"

    text = (
        f"Группа: {group}\n"
        f"Уровней: {g.get('levels','нет')}\n"
        f"Дистанция XP: {g.get('distance','нет')}\n\n"
        f"Названия:\n{names}"
    )

    await call.message.answer(text)