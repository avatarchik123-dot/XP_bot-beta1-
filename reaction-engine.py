from config import MAX_REACTION_XP_PER_MESSAGE

reaction_counter = {}

def add_reaction_xp(message_id, user_id):
    if message_id not in reaction_counter:
        reaction_counter[message_id] = 0
    if reaction_counter[message_id] >= MAX_REACTION_XP_PER_MESSAGE:
        return False
    reaction_counter[message_id] += 1
    return True