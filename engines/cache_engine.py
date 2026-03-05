from datetime import datetime, timedelta

cache = {}

def set_cache(key, value, ttl_seconds=30):
    expire = datetime.now() + timedelta(seconds=ttl_seconds)
    cache[key] = {"value": value, "expire": expire}

def get_cache(key):
    data = cache.get(key)
    if not data:
        return None
    if datetime.now() > data["expire"]:
        del cache[key]
        return None
    return data["value"]

def invalidate_cache(key):
    if key in cache:
        del cache[key]