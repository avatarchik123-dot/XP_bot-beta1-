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
    get_level_names,
    set_level_pic
)

router = Router()


# ---------------- FSM ----------------

class SetupStates(StatesGroup):

    waiting_levels = State()
    waiting_distance = State()
    waiting_names = State()

    confirm = State()

    waiting_pic = State()


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


def menu_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Количество уровней", callback_data="levels")],
            [InlineKeyboardButton(text="📏 Дистанция XP", callback_data="distance")],
            [InlineKeyboardButton(text="🏷 Названия уровней", callback_data="names")],
            [InlineKeyboardButton(text="📋 Текущие параметры", callback_data="current")]
        ]
    )


def confirm_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )


# ---------------- РЕГИСТРАЦИЯ ГРУПП ----------------

@router.my_chat_member()
async def bot_added(event):

    chat = event.chat

    if chat.type not in ["group", "supergroup"]:
        return

    add_group(chat.id, chat.title)


# ---------------- SETTINGS ----------------

@router.message(Command("settings"))
async def settings(message: Message):

    await message.answer(
        "Выберите группу",
        reply_markup=groups_keyboard()
    )


# ---------------- ВЫБОР ГРУППЫ ----------------

@router.callback_query(F.data.startswith("group_"))
async def choose_group(call: CallbackQuery, state: FSMContext):

    gid = int(call.data.split("_")[1])

    await state.update_data(group=gid)

    await call.message.edit_text(
        "⚙️ Меню настроек",
        reply_markup=menu_keyboard()
    )


# ---------------- КОЛИЧЕСТВО УРОВНЕЙ ----------------

@router.callback_query(F.data == "levels")
async def levels(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_levels)

    await call.message.answer(
        "Введите количество уровней (5-100)"
    )


@router.message(SetupStates.waiting_levels)
async def levels_value(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    value = int(message.text)

    if value < 5 or value > 100:
        await message.answer("Допустимо: 5 - 100")
        return

    await state.update_data(temp_levels=value, action="levels")

    await message.answer(
        f"Установить {value} уровней?",
        reply_markup=confirm_keyboard()
    )


# ---------------- ДИСТАНЦИЯ ----------------

@router.callback_query(F.data == "distance")
async def distance(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_distance)

    await call.message.answer(
        "Введите дистанцию XP между уровнями"
    )


@router.message(SetupStates.waiting_distance)
async def distance_value(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    value = int(message.text)

    await state.update_data(temp_distance=value, action="distance")

    await message.answer(
        f"Установить дистанцию {value} XP?",
        reply_markup=confirm_keyboard()
    )


# ---------------- НАЗВАНИЯ ----------------

@router.callback_query(F.data == "names")
async def names(call: CallbackQuery, state: FSMContext):

    await state.set_state(SetupStates.waiting_names)

    await call.message.answer(
        "Введите названия уровней:\n\n"
        "1. Новичок\n"
        "2. Актив\n"
        "3. Флудер"
    )


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

    await state.update_data(temp_names=names, action="names")

    await message.answer(
        "Сохранить названия?",
        reply_markup=confirm_keyboard()
    )


# ---------------- ПОДТВЕРЖДЕНИЕ ----------------

@router.callback_query(F.data == "confirm")
async def confirm(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    group = data.get("group")
    action = data.get("action")

    if action == "levels":
        set_levels(group, data["temp_levels"])

    if action == "distance":
        set_distance(group, data["temp_distance"])

    if action == "names":
        set_level_names(group, data["temp_names"])

    await call.message.answer(
        "✅ Настройки сохранены",
        reply_markup=menu_keyboard()
    )

    await state.clear()


# ---------------- ОТМЕНА ----------------

@router.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery, state: FSMContext):

    await call.message.answer(
        "❌ Изменение отменено",
        reply_markup=menu_keyboard()
    )

    await state.clear()


# ---------------- ТЕКУЩИЕ ПАРАМЕТРЫ ----------------

@router.callback_query(F.data == "current")
async def current(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    gid = data.get("group")

    settings = get_settings(gid)
    names = get_level_names(gid)

    text = f"Группа: {gid}\n"
    text += f"Уровней: {settings.get('levels')}\n"
    text += f"Дистанция XP: {settings.get('distance')}\n\n"

    text += "Названия уровней:\n"

    for lvl, name in names.items():
        text += f"{lvl}. {name}\n"

    await call.message.answer(text)


# ---------------- SETPIC ----------------

@router.message(Command("setpic"))
async def setpic(message: Message, state: FSMContext):

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование: /setpic 3")
        return

    if not args[1].isdigit():
        await message.answer("Уровень должен быть числом")
        return

    level = int(args[1])

    await state.update_data(pic_level=level)

    await state.set_state(SetupStates.waiting_pic)

    await message.answer(
        f"Отправьте картинку для уровня {level}"
    )


@router.message(SetupStates.waiting_pic)
async def save_pic(message: Message, state: FSMContext):

    if not message.photo:
        await message.answer("Отправьте изображение")
        return

    data = await state.get_data()

    level = data["pic_level"]
    group = data["group"]

    file_id = message.photo[-1].file_id

    set_level_pic(group, level, file_id)

    await message.answer("✅ Картинка сохранена")

    await state.clear()