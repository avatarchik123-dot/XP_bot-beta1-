from config import TEXT_XP_TABLE, MEDIA_XP

def calculate_text_xp(text):
    length = len(text)
    for min_len, max_len, xp in TEXT_XP_TABLE:
        if min_len <= length <= max_len:
            return xp
    return 0

def calculate_media_xp(message):
    xp = 0
    if message.photo:
        xp += MEDIA_XP["photo"]
    if message.video:
        xp += MEDIA_XP["video"]
    if message.sticker:
        xp += MEDIA_XP["sticker"]
    if message.animation:
        xp += MEDIA_XP["gif"]
    if message.voice:
        xp += MEDIA_XP["voice"]
    return xp

def can_gain_xp(user_id, group_id, last_time, anti_spam_seconds):
    import asyncio
    now = asyncio.get_event_loop().time()
    if last_time and now - last_time < anti_spam_seconds:
        return False
    return True