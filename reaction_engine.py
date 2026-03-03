from level_engine import add_xp
from config import MAX_REACTION_XP

def on_reaction(user_id, group_id, reactions_count):
    xp = min(reactions_count, MAX_REACTION_XP)
    add_xp(user_id, group_id, xp)