from services.database import level_settings


def get_settings(chat_id):

    data = level_settings.get(level_settings.chat_id == chat_id)

    if not data:
        data = {
            "chat_id": chat_id,
            "level_count": 20,
            "xp_step": 100,
            "level_names": {},
            "level_images": {}
        }

        level_settings.insert(data)

    return data


def set_level_count(chat_id, count):

    level_settings.update(
        {"level_count": count},
        level_settings.chat_id == chat_id
    )


def set_xp_step(chat_id, step):

    level_settings.update(
        {"xp_step": step},
        level_settings.chat_id == chat_id
    )


def set_level_names(chat_id, names):

    level_settings.update(
        {"level_names": names},
        level_settings.chat_id == chat_id
    )


def set_level_image(chat_id, level, file_id):

    data = get_settings(chat_id)

    images = data.get("level_images", {})

    images[level] = file_id

    level_settings.update(
        {"level_images": images},
        level_settings.chat_id == chat_id
    )