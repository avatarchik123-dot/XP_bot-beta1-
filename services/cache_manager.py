import time

user_cooldowns = {}


def check_antiflood(user_id):

    now = time.time()

    last = user_cooldowns.get(user_id)

    if last and now - last < 3:
        return False

    user_cooldowns[user_id] = now

    return True