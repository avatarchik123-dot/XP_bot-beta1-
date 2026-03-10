from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from services.database import set_level_pic, get_level_pic, get_groups

router = Router()

# ожидание картинки
waiting_picture = {}


# ---------- команда ----------

@router.message(Command("setlevelpic"))
async def set_level_pic_start(message: Message):

    if message.chat.type != "private":
        await message.answer("Команду нужно писать боту в личку")
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Используй: /setlevelpic УРОВЕНЬ")
        return

    try:
        level = int(args[1])
    except:
        await message.answer("Уровень должен быть числом")
        return

    groups = get_groups()

    if not groups:
        await message.answer("Бот не добавлен ни в одну группу")
        return

    buttons = []

    for g in groups:

        title = g.get("title", str(g["chat_id"]))

        buttons.append([
            InlineKeyboardButton(
                text=title,
                callback_data=f"lvlpic_{g['chat_id']}_{level}"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        "Для какой группы установить картинку?",
        reply_markup=keyboard
    )


# ---------- выбор группы ----------

@router.callback_query(F.data.startswith("lvlpic_"))
async def choose_group(call: CallbackQuery):

    data = call.data.split("_")

    chat_id = int(data[1])
    level = int(data[2])

    waiting_picture[call.from_user.id] = {
        "chat_id": chat_id,
        "level": level
    }

    await call.message.answer(
        "Отправьте фото или GIF для этого уровня"
    )

    await call.answer()


# ---------- получение картинки ----------

@router.message()
async def receive_picture(message: Message):

    user_id = message.from_user.id

    if user_id not in waiting_picture:
        return

    data = waiting_picture[user_id]

    chat_id = data["chat_id"]
    level = data["level"]

    file_id = None

    if message.photo:
        file_id = message.photo[-1].file_id

    elif message.animation:
        file_id = message.animation.file_id

    elif message.document:
        file_id = message.document.file_id

    if not file_id:
        await message.answer("Нужно отправить фото или GIF")
        return

    set_level_pic(chat_id, level, file_id)

    del waiting_picture[user_id]

    await message.answer("✅ Изменения успешно сохранены")

async def send_level_picture(message: Message, level: int, text: str):

    chat_id = message.chat.id

    file_id = get_level_pic(chat_id, level)

    if not file_id:
        await message.answer(text)
        return

    try:

        await message.answer_animation(
            file_id,
            caption=text
        )

    except:

        await message.answer_photo(
            file_id,
            caption=text
        )