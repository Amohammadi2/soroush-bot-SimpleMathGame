from threading import Thread
from client import Client 
from token_loader import load_token
from executer import Executer
from logger import Logger
from guards import max_message_len, allow_message_types
from admin_commands import cmds

EXECUTERS = dict()
LOG_FILE = open("../log/log.txt", "a+", encoding="utf-8")
LOGGER = Logger(LOG_FILE)


@max_message_len(256)
@allow_message_types(["TEXT"])
def process_message(bot, msg, **kwargs):
    user_id = msg["from"]
    if msg["body"] == "start":
        EXECUTERS[user_id] = Executer(bot, user_id)
        EXECUTERS[user_id].start_game()
    elif msg["body"].lstrip("-+").isdigit():
        EXECUTERS[user_id].process_response(msg)
    for cmd in cmds.keys():
        if cmd in msg["body"]:
            cmd_args = msg["body"].split()[2::]
            print (cmd)
            cmds[cmd](*cmd_args)

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