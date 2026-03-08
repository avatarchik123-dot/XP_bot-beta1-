from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import sqlite3

router = Router()

DB_PATH = "data/bot.db"


# ---------------- БАЗА ----------------

def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():

    db = get_db()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS known_groups(
        chat_id INTEGER PRIMARY KEY,
        title TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS level_settings(
        chat_id INTEGER PRIMARY KEY,
        levels INTEGER,
        distance INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS level_names(
        chat_id INTEGER,
        level INTEGER,
        name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS level_pics(
        chat_id INTEGER,
        level INTEGER,
        file_id TEXT
    )
    """)

    db.commit()
    db.close()


init_db()


# ---------------- FSM ----------------

class SetupStates(StatesGroup):

    waiting_levels = State()
    confirm_levels = State()

    waiting_distance = State()
    confirm_distance = State()

    waiting_names = State()
    confirm_names = State()

    waiting_pic = State()


# ---------------- КЛАВИАТУРЫ ----------------

def groups_keyboard():

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT chat_id,title FROM known_groups")

    buttons = []

    for gid,title in cur.fetchall():

        buttons.append([
            InlineKeyboardButton(
                text=title,
                callback_data=f"group_{gid}"
            )
        ])

    db.close()

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def menu_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Количество уровней",callback_data="set_levels")],
            [InlineKeyboardButton(text="📏 Дистанция XP",callback_data="set_distance")],
            [InlineKeyboardButton(text="🏷 Названия уровней",callback_data="set_names")],
            [InlineKeyboardButton(text="📋 Текущие параметры",callback_data="current")]
        ]
    )


def confirm_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить",callback_data="confirm")],
            [InlineKeyboardButton(text="❌ Отмена",callback_data="cancel")]
        ]
    )


# ---------------- РЕГИСТРАЦИЯ ГРУПП ----------------

@router.my_chat_member()
async def bot_added(event):

    chat = event.chat

    if chat.type not in ["group","supergroup"]:
        return

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO known_groups(chat_id,title) VALUES (?,?)",
        (chat.id,chat.title)
    )

    db.commit()
    db.close()


# ---------------- SETTINGS ----------------

@router.message(Command("settings"))
async def settings(message: Message):

    await message.answer(
        "Выберите группу",
        reply_markup=groups_keyboard()
    )


# ---------------- ВЫБОР ГРУППЫ ----------------

@router.callback_query(F.data.startswith("group_"))
async def choose_group(call: CallbackQuery,state:FSMContext):

    gid = int(call.data.split("_")[1])

    await state.update_data(group=gid)

    await call.message.edit_text(
        "⚙️ Меню настроек",
        reply_markup=menu_keyboard()
    )


# ---------------- УРОВНИ ----------------

@router.callback_query(F.data=="set_levels")
async def set_levels(call:CallbackQuery,state:FSMContext):

    await state.set_state(SetupStates.waiting_levels)

    await call.message.answer(
        "Укажите количество уровней (5-100)"
    )


@router.message(SetupStates.waiting_levels)
async def levels_value(message:Message,state:FSMContext):

    try:

        value=int(message.text)

        if value<5 or value>100:
            await message.answer("Можно от 5 до 100")
            return

        await state.update_data(temp_levels=value)

        await state.set_state(SetupStates.confirm_levels)

        await message.answer(
            f"Установить {value} уровней?",
            reply_markup=confirm_keyboard()
        )

    except:
        await message.answer("Введите число")


# ---------------- ДИСТАНЦИЯ XP ----------------

@router.callback_query(F.data=="set_distance")
async def set_distance(call:CallbackQuery,state:FSMContext):

    await state.set_state(SetupStates.waiting_distance)

    await call.message.answer(
        "Введите дистанцию XP между уровнями"
    )


@router.message(SetupStates.waiting_distance)
async def distance_value(message:Message,state:FSMContext):

    try:

        value=int(message.text)

        await state.update_data(temp_distance=value)

        await state.set_state(SetupStates.confirm_distance)

        await message.answer(
            f"Установить дистанцию {value} XP?",
            reply_markup=confirm_keyboard()
        )

    except:
        await message.answer("Введите число")


# ---------------- НАЗВАНИЯ ----------------

@router.callback_query(F.data=="set_names")
async def set_names(call:CallbackQuery,state:FSMContext):

    await state.set_state(SetupStates.waiting_names)

    await call.message.answer(
        "Введите названия:\n\n"
        "1. Новичок\n"
        "2. Актив\n"
        "3. Флудер"
    )


@router.message(SetupStates.waiting_names)
async def names_value(message:Message,state:FSMContext):

    names={}

    for line in message.text.split("\n"):

        if "." not in line:
            continue

        num,name=line.split(".",1)

        try:
            names[int(num.strip())]=name.strip()
        except:
            pass

    await state.update_data(temp_names=names)

    await state.set_state(SetupStates.confirm_names)

    await message.answer(
        "Сохранить названия?",
        reply_markup=confirm_keyboard()
    )


# ---------------- ПОДТВЕРЖДЕНИЕ ----------------

@router.callback_query(F.data=="confirm")
async def confirm(call:CallbackQuery,state:FSMContext):

    data=await state.get_data()

    group=data["group"]

    db=get_db()
    cur=db.cursor()

    if "temp_levels" in data:

        cur.execute("""
        INSERT INTO level_settings(chat_id,levels)
        VALUES (?,?)
        ON CONFLICT(chat_id)
        DO UPDATE SET levels=excluded.levels
        """,(group,data["temp_levels"]))

    if "temp_distance" in data:

        cur.execute("""
        INSERT INTO level_settings(chat_id,distance)
        VALUES (?,?)
        ON CONFLICT(chat_id)
        DO UPDATE SET distance=excluded.distance
        """,(group,data["temp_distance"]))

    if "temp_names" in data:

        cur.execute(
            "DELETE FROM level_names WHERE chat_id=?",
            (group,)
        )

        for lvl,name in data["temp_names"].items():

            cur.execute(
                "INSERT INTO level_names VALUES (?,?,?)",
                (group,lvl,name)
            )

    db.commit()
    db.close()

    await call.message.answer(
        "Настройки сохранены",
        reply_markup=menu_keyboard()
    )

    await state.clear()


# ---------------- ОТМЕНА ----------------

@router.callback_query(F.data=="cancel")
async def cancel(call:CallbackQuery,state:FSMContext):

    await call.message.answer(
        "Изменение отменено",
        reply_markup=menu_keyboard()
    )

    await state.clear()


# ---------------- ТЕКУЩИЕ ПАРАМЕТРЫ ----------------

@router.callback_query(F.data=="current")
async def current(call:CallbackQuery,state:FSMContext):

    data=await state.get_data()

    gid=data["group"]

    db=get_db()
    cur=db.cursor()

    cur.execute(
        "SELECT levels,distance FROM level_settings WHERE chat_id=?",
        (gid,)
    )

    settings=cur.fetchone()

    cur.execute(
        "SELECT level,name FROM level_names WHERE chat_id=?",
        (gid,)
    )

    names=cur.fetchall()

    db.close()

    text=f"Группа: {gid}\n"

    if settings:
        text+=f"Уровней: {settings[0]}\n"
        text+=f"Дистанция XP: {settings[1]}\n"

    text+="\nНазвания:\n"

    for lvl,name in names:
        text+=f"{lvl}. {name}\n"

    await call.message.answer(text)


# ---------------- SETPIC ----------------

@router.message(Command("setpic"))
async def setpic(message:Message,state:FSMContext):

    args=message.text.split()

    if len(args)<2:
        await message.answer("Использование: /setpic номер_уровня")
        return

    level=int(args[1])

    await state.update_data(pic_level=level)

    await state.set_state(SetupStates.waiting_pic)

    await message.answer(
        f"Отправьте картинку или GIF для уровня {level}"
    )


@router.message(SetupStates.waiting_pic)
async def save_pic(message:Message,state:FSMContext):

    data=await state.get_data()

    level=data["pic_level"]
    group=data.get("group")

    if not message.photo and not message.animation:
        await message.answer("Нужно фото или gif")
        return

    file_id = message.photo[-1].file_id if message.photo else message.animation.file_id

    db=get_db()
    cur=db.cursor()

    cur.execute(
        "INSERT INTO level_pics VALUES (?,?,?)",
        (group,level,file_id)
    )

    db.commit()
    db.close()

    await message.answer("Картинка уровня сохранена")

    await state.clear()