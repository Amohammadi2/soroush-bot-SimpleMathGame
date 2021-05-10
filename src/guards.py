from functools import wraps
from logger import Logger

GOING_TO_BE_BANNED = []
BANNED = []
LOG_FILE = open("../log/log.txt", "a+", encoding="utf-8")
LOGGER = Logger(LOG_FILE)

def max_message_len(length):
    def decorator(fn):
        def wrapper(bot, msg, *args, **kwargs):
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