import os

GROUPS_FILE = "groups.json"
LEVELS_FILE = "levels.json"
LEVELS_BACKUP = "levels_backup.json"
TEMP_SETUP = "temp_setup.json"

MEDIA_FOLDER = "media/"
USERS_FOLDER = "users/"

ANTI_SPAM_SECONDS = 3
MAX_REACTION_XP = 50

# Текст XP
TEXT_XP_TABLE = [
    (3, 9, 1),
    (10, 29, 2),
    (30, 49, 3),
    (50, 10000, 5)
]

# Медиа XP
MEDIA_XP = {
    "photo": 3,
    "video": 5,
    "sticker": 0,
    "gif": 0,
    "voice": 0
}

# Стандартные уровни (если нужны)
DEFAULT_LEVELS = [
    {"name": "Новичок", "xp": 100},
    {"name": "Активный", "xp": 300}
]

CACHE_TOP_SECONDS = 30
MAX_LOGS_PER_GROUP = 100