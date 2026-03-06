from config import *

def calc_xp_text(length):

    if 3 <= length <= 20:
        return 1

    if 21 <= length <= 50:
        return 3

    if length >= 51:
        return 5

    return 0