import aiosqlite
from config import DB_NAME


async def db():

    return await aiosqlite.connect(DB_NAME)