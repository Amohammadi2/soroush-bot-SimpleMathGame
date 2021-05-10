from functools import partial

class Logger:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            return super().__new__(cls)
        return instance

    def __init__(self, log_file, log_to_console = True):
        self.log_file = log_file
        self.log_to_console = log_to_console
        self.log = partial(self.__log, "log")
        self.warning = partial(self.__log, "warning")
        self.error = partial(self.__log, "warning")

    def __log(self, type: str, msg: str):
        log_msg = f"[{type.upper()}] {msg}"
        if self.log_to_console:
            print (log_msg)
        self.log_file.write("{}\n".format(log_msg))

    def __del__(self):
        self.log_file.close()