import time

cache = {}

def get(key):
    if key in cache:
        data, ts = cache[key]
        if time.time() - ts < 30:
            return data
    return None

def set(key, value):
    cache[key] = (value, time.time())

def invalidate(key):
    if key in cache:
        del cache[key]