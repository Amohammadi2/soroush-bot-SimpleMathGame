from functools import wraps
import time
from random import choice
from logger import Logger

LOG_FILE = open("../log/log.txt", "a+", encoding="utf-8")
LOGGER = Logger(LOG_FILE)


class Executer:
    def __init__(self, bot, user_id):
        self.bot = bot
        self.nums = [x for x in range(1, 10)]
        self.oper = ["*", "+", "-"]
        self.user_id = user_id

    def start_game(self):
        LOGGER.log(f"game started. user_id={self.user_id}")
        self.bot.send_text(self.user_id,
            "شما فقط 5 ثانیه برای پاسخ دادن وقت دارید"
        )
        self.start()

    def game_over(self, response, message):
        self.bot.send_text(
            response["from"],
            message
        )

    def start(self):
        response = self.get_random_math_problem()
        self.answer = eval(response)
        self.bot.send_text(self.user_id, response)
        self.start_time = time.perf_counter()

    def process_response(self, response):
        if getattr(self, "answer", None) is None:
            return
        elapsed = time.perf_counter() - self.start_time
        if elapsed > 5:
            self.game_over(response, "تایم شما به اتمام رسید")
            return

        if int(response["body"]) == self.answer:
            LOGGER.log("answer was true: {} | user={}".format(self.answer, self.user_id))
            self.start()
            return
        LOGGER.log("answer was false: {} | user={}".format(self.answer, self.user_id))
        self.game_over(response, 'بازی را باختید، جواب مورد انتظار={}'.format(self.answer))

    def get_random_math_problem(self):
        n = choice([3,5])
        return " ".join([
            str(choice(self.nums)) if x%2==1 else choice(self.oper)
            for x in range(1, n+1)
        ])