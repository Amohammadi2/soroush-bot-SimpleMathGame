from functools import wraps
import time
from random import choice

def time_protect(time):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, msg, *args, **kwargs):
            print ("LOG [time_protect]:",msg)
            return fn(self, msg, *args, **kwargs)
        return wrapper
    return decorator

class Executer:
    def __init__(self, bot):
        self.bot = bot
        self.nums = [x for x in range(1, 10)]
        self.oper = ["*", "+", "-"]

    def start_game(self, message):
        self.bot.send_text(message["from"],
            "شما فقط 5 ثانیه برای پاسخ دادن وقت دارید"
        )
        self.start(message)

    @time_protect(60*60*24)
    def start(self, message):
        response = self.get_random_math_problem()
        self.answer = eval(response)
        self.bot.send_text(message["from"], response)
        self.start_time = time.perf_counter()

    def process_response(self, response):
        self.elapsed = time.perf_counter() - self.start_time
        if int(response["body"]) == self.answer:
            print ("answer was true")
            self.start(response)
            return
        
        self.bot.send_text(
            response["from"],
            'بازی را باختید، جواب مورد انتظار={}'.format(self.answer)
        )

    def get_random_math_problem(self):
        n = choice([3,5])
        return " ".join([
            str(choice(self.nums)) if x%2==1 else choice(self.oper)
            for x in range(1, n+1)
        ])