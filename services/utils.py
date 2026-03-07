import asyncio


async def send_temp(message, text, seconds=60):

    msg = await message.answer(text)

    await asyncio.sleep(seconds)

    try:
        await msg.delete()
    except:
        pass