from config import *

def text_xp(text):

    length = len(text)

    for min_l, max_l, xp in XP_TEXT:
        if min_l <= length <= max_l:
            return xp

    return 0