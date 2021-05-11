from functools import wraps
from contextlib import suppress
from logger import Logger

GOING_TO_BE_BANNED = []
BANNED = []
LOG_FILE = open("../log/log.txt", "a+", encoding="utf-8")
LOGGER = Logger(LOG_FILE)

def max_message_len(length):
    def decorator(fn):
        if not fn: return
        def wrapper(bot, msg, *args, **kwargs):
            LOGGER.log(msg)
            LOGGER.log(f"GB users: {GOING_TO_BE_BANNED}")
            LOGGER.log(f"B users: {BANNED}")
            user_id = msg["from"]
            if user_id in BANNED:
                return
            if len(msg["body"]) > length:
                # first time -> warning
                if user_id in GOING_TO_BE_BANNED:
                    LOGGER.warning("user {} has been banned".format(user_id))
                    bot.send_text(user_id, "شما بن شدید. زین پس پاسخی به پیام های شما داده نخواهد شد")
                    BANNED.append(user_id)
                    return
                # second time -> ban the user
                LOGGER.warning("user: {} is going to be banned".format(user_id))
                bot.send_text(user_id, "ورودی بیش ازحد، در صورت تکرار بن خواهید شد")
                GOING_TO_BE_BANNED.append(user_id)
                return
            return fn(bot, msg, *args, **kwargs)
        return wrapper
    return decorator

def allow_message_types(type_list: list):
    def decorator(fn):
        if not fn: return
        @wraps(fn)
        def wrapper(bot, msg, *args, **kwargs):
            if msg["type"] in type_list: return fn(bot, msg, *args, **kwargs)

        return wrapper
    return decorator

def noexcept(excep_type):
    def decorator(fn):
        if not fn: return
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with suppress(excep_type):
                return fn(*args, **kwargs)
        return wrapper
    return decorator