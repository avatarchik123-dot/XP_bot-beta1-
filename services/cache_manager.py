import time

cooldowns = {}

def antiflood(user_id, delay):

    now = time.time()

    last = cooldowns.get(user_id)

    if last and now - last < delay:
        return False

    cooldowns[user_id] = now
    return True