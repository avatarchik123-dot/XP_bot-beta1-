from storage import load, save

def get_user_data(group_id, user_id):
    levels = load("levels.json")
    group_id = str(group_id)
    user_id = str(user_id)

    if group_id not in levels:
        levels[group_id] = {}

    if user_id not in levels[group_id]:
        levels[group_id][user_id] = {"xp": 0, "level": 0}

    save("levels.json", levels)
    return levels[group_id][user_id]

def add_xp(group_id, user_id, amount):
    levels = load("levels.json")
    group_id = str(group_id)
    user_id = str(user_id)

    user = get_user_data(group_id, user_id)
    user["xp"] += amount

    levels[group_id][user_id] = user
    save("levels.json", levels)