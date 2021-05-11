from functools import partial, wraps
import datetime

class Logger:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            return super().__new__(cls)
        return cls.instance

    def __init__(self, log_file, log_to_console = True):
        self.log_file = log_file
        self.log_to_console = log_to_console
        self.log = partial(self.__log, "log")
        self.warning = partial(self.__log, "warning")
        self.error = partial(self.__log, "warning")

    def __log(self, type: str, msg: str):
        log_msg = f"[{type.upper()}] date/time:{datetime.datetime.now()} {msg}"
        if self.log_to_console:
            print (log_msg)
        self.log_file.write("{}\n".format(log_msg))
        self.log_file.flush()

    def __del__(self):
        self.log_file.close()

def log_on_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        Logger(open("../log/log.txt", "a+")).log(f"call to function: {fn.__name__}| ({args}, {kwargs})")
        return fn(*args, **kwargs)
    return wrapper