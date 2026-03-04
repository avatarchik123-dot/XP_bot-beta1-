def get_level(xp, levels):
    current_level = 0
    for lvl, data in levels.items():
        if xp >= data["xp"]:
            current_level = lvl
    return current_level