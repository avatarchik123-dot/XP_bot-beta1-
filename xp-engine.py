import time
from config import ANTI_SPAM_SECONDS
from storage import load, save

last_message_time = {}
last_messages = {}

def calculate_text_xp(text):
    if not text:
        return 0
    length = len(text.strip())
    if length < 3:
        return 0
    if length < 10:
        return 1
    if length < 30:
        return 2
    if length < 50:
        return 3
    return 5

def calculate_media_xp(message):
    xp = 0
    if message.photo:
        xp += 3
    if message.video:
        xp += 5
    return xp

def can_gain_xp(user_id):
    now = time.time()
    if user_id not in last_message_time:
        last_message_time[user_id] = now
        return True
    if now - last_message_time[user_id] >= ANTI_SPAM_SECONDS:
        last_message_time[user_id] = now
        return True
    return False