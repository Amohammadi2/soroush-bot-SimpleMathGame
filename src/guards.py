from functools import wraps
from contextlib import suppress
from logger import Logger
import time

GOING_TO_BE_BANNED = []
BANNED = []
LOG_FILE = open("../log/log.txt", "a+", encoding="utf-8")
LOGGER = Logger(LOG_FILE)

def check_fn_exists(dec):
    @wraps(dec)
    def wrapper(fn):
        if not fn: return
        return dec(fn)
    return wrapper

def max_message_len(length):
    @check_fn_exists
    def decorator(fn):
        def wrapper(bot, msg, *args, **kwargs):
            LOGGER.log(msg)
            LOGGER.log(f"GB users: {GOING_TO_BE_BANNED}")
            LOGGER.log(f"B users: {BANNED}")
            user_id = msg["from"]
            tm = msg["time"]
            for x in BANNED:
                if time.time() - int(x["time"]) / 1000 > 86400: # it's been more than a day
                    BANNED.remove(x)
                    break
                if x["id"] == user_id: return

            if len(msg["body"]) > length:
                # first time -> warning
                if user_id in GOING_TO_BE_BANNED:
                    LOGGER.warning("user {} has been banned".format(user_id))
                    bot.send_text(user_id, "شما بن شدید. زین پس پاسخی به پیام های شما داده نخواهد شد")
                    BANNED.append({"id":user_id, "time": tm})
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
    @check_fn_exists
    def decorator(fn):
        @wraps(fn)
        def wrapper(bot, msg, *args, **kwargs):
            if msg["type"] in type_list: return fn(bot, msg, *args, **kwargs)
        return wrapper
    return decorator


def noexcept(excep_type):
    @check_fn_exists
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with suppress(excep_type):
                return fn(*args, **kwargs)
        return wrapper
    return decorator

def time_limit(_time):
    @check_fn_exists
    def decorator(fn):
        @wraps(fn)
        def wrapper(bot, msg, *args, **kwargs):
            m_time = int(msg["time"]) / 1000 # convert to seconds
            if (exp_bool:=(exp:=time.time() - m_time) > _time):
                print ("time limit hit")
                return
            print (exp, exp_bool)
            print (_time)
            return fn(bot, msg, *args, **kwargs)
        return wrapper
    return decorator