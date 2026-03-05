from aiogram import Router

router = Router()

from aiogram import types
from services.file_manager import load, save

def register_reaction_handlers(dp):

    @dp.message_reaction()
    async def handle_reaction(event: types.MessageReactionUpdated):
        group_id = str(event.chat.id)
        user_id = str(event.user.id)
        message_author = str(event.message.from_user.id)

        groups = load("groups.json")

        if group_id not in groups:
            return

        users = groups[group_id]["users"]

        if message_author not in users:
            return

        current_xp = users[message_author]["xp"]

        users[message_author]["xp"] = current_xp + 1

        save("groups.json", groups)