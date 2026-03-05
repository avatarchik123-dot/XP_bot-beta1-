from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda m: m.text == "/setup")
async def setup_start(message: Message):

    await message.answer(
        "Настройка бота будет доступна позже"
    )