from storage import load, save
from config import MAX_LOGS

def add_log(group_id, text):
    groups = load("groups.json")
    group_id = str(group_id)

    if group_id not in groups:
        groups[group_id] = {"logs": []}

    groups[group_id]["logs"].append(text)
    groups[group_id]["logs"] = groups[group_id]["logs"][-MAX_LOGS:]

    save("groups.json", groups)