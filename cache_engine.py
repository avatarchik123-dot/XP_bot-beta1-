import time
from config import CACHE_TOP_SECONDS

top_cache = {}

def get_top_cache(group_id):
    data = top_cache.get(group_id)
    if data and time.time() - data["timestamp"] < CACHE_TOP_SECONDS:
        return data["value"]
    return None

def update_top_cache(group_id, value):
    top_cache[group_id] = {"value": value, "timestamp": time.time()}