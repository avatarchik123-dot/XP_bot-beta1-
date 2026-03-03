import time
from config import TOP_CACHE_SECONDS

top_cache = {}

def get_cached_top(group_id):
    if group_id in top_cache:
        data, timestamp = top_cache[group_id]
        if time.time() - timestamp < TOP_CACHE_SECONDS:
            return data
    return None

def set_cached_top(group_id, data):
    top_cache[group_id] = (data, time.time())