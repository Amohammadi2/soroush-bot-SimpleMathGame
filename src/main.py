from threading import Thread
from client import Client 
from token_loader import load_token
from executer import Executer
from logger import Logger
from guards import max_message_len

EXECUTERS = dict()
LOG_FILE = open("../log/log.txt", "a+", encoding="utf-8")
LOGGER = Logger(LOG_FILE)


@max_message_len(20)
def process_message(bot, msg, **kwargs):
    LOGGER.log(msg)
    user_id = msg["from"]
    if msg["body"] == "start":
        EXECUTERS[user_id] = Executer(bot, user_id)
        EXECUTERS[user_id].start_game()
    elif msg["body"].lstrip("-+").isdigit():
        EXECUTERS[user_id].process_response(msg)

def message_loop(messages_iter, bot):
    for msg in messages_iter:
        process_message(bot, msg)

def main():
    token = load_token()
    bot = Client(token)

    try:
        messages = bot.get_messages()
        message_loop(messages, bot)
    

    except KeyboardInterrupt:
        exit()
    except Exception as e:
        raise e

if __name__ == "__main__": main()