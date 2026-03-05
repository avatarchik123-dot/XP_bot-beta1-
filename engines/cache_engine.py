import time

cache = {}


def set_cache(key, value, ttl=30):
    cache[key] = {
        "value": value,
        "expire": time.time() + ttl
    }


def get_cache(key):
    data = cache.get(key)

    if not data:
        return None

    if time.time() > data["expire"]:
        del cache[key]
        return None

    return data["value"]