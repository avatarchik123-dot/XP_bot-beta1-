from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.database import (
    add_group,
    get_groups,
    set_levels,
    set_distance,
    set_level_names,
    get_settings,
    get_level_names
)

router = Router()


# ---------------- FSM ----------------

class SetupStates(StatesGroup):

    choosing_group = State()

    waiting_levels = State()
    waiting_distance = State()
    waiting_names = State()

    confirm = State()


# ---------------- КЛАВИАТУРЫ ----------------

def groups_keyboard():

    buttons = []

    for g in get_groups():

        title = g.get("title", str(g["chat_id"]))

        buttons.append([
            InlineKeyboardButton(
                text=title,
                callback_data=f"group_{g['chat_id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
            [InlineKeyboardButton(text="↩ Назад", callback_data="cancel")]
        ]
    )


# ---------------- РЕГИСТРАЦИЯ ГРУПП ----------------

@router.my_chat_member()
async def bot_added(event):

    chat = event.chat

    if chat.type not in ["group", "supergroup"]:
        return

    add_group(chat.id, chat.title)


# ---------------- START SETTINGS ----------------

@router.message(Command("settings"))
async def settings(message: Message, state: FSMContext):

    await state.set_state(SetupStates.choosing_group)

    await message.answer(
        "Выберите группу для настройки",
        reply_markup=groups_keyboard()
    )


# ---------------- ВЫБОР ГРУППЫ ----------------

@router.callback_query(F.data.startswith("group_"))
async def choose_group(call: CallbackQuery, state: FSMContext):

    gid = int(call.data.split("_")[1])

    await state.update_data(group=gid)

    await state.set_state(SetupStates.waiting_levels)

    await call.message.answer(
        "Введите количество уровней (5-100)"
    )


# ---------------- УРОВНИ ----------------

@router.message(SetupStates.waiting_levels)
async def levels_value(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    value = int(message.text)

    if value < 5 or value > 100:
        await message.answer("Допустимо: 5 - 100")
        return

    await state.update_data(levels=value)

    await state.set_state(SetupStates.waiting_distance)

    await message.answer(
        "Введите дистанцию XP между уровнями\n\n"
        "Например: 250"
    )


# ---------------- ДИСТАНЦИЯ ----------------

@router.message(SetupStates.waiting_distance)
async def distance_value(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    value = int(message.text)

    await state.update_data(distance=value)

    await state.set_state(SetupStates.waiting_names)

    await message.answer(
        "Введите названия уровней:\n\n"
        "1. Новичок\n"
        "2. Актив\n"
        "3. Флудер"
    )


# ---------------- НАЗВАНИЯ ----------------

@router.message(SetupStates.waiting_names)
async def names_value(message: Message, state: FSMContext):

    names = {}

    for line in message.text.split("\n"):

        if "." not in line:
            continue

        num, name = line.split(".", 1)

        try:
            lvl = int(num.strip())
        except:
            continue

        names[lvl] = name.strip()

    if not names:
        await message.answer("Не удалось распознать формат")
        return

    await state.update_data(names=names)

    data = await state.get_data()

    text = "⚙️ Проверьте настройки:\n\n"
    text += f"Уровней: {data['levels']}\n"
    text += f"XP между уровнями: {data['distance']}\n\n"
    text += "Названия уровней:\n"

    for lvl, name in names.items():
        text += f"{lvl}. {name}\n"

    await state.set_state(SetupStates.confirm)

    await message.answer(
        text,
        reply_markup=confirm_keyboard()
    )


# ---------------- ПОДТВЕРЖДЕНИЕ ----------------

@router.callback_query(F.data == "confirm")
async def confirm(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    group = data["group"]

    set_levels(group, data["levels"])
    set_distance(group, data["distance"])
    set_level_names(group, data["names"])

    await call.message.answer(
        "✅ Настройки сохранены"
    )

    await state.clear()


# ---------------- ОТМЕНА ----------------

@router.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery, state: FSMContext):

    await call.message.answer(
        "Настройка отменена. Запустите /settings заново."
    )

    await state.clear()