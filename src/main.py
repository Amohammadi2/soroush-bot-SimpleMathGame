from client import Client 
from token_loader import load_token
from executer import Executer
from threading import Thread


def message_loop(messages_iter, bot):
    executer = Executer(bot)
    for msg in messages_iter:
        if msg["body"] == "start":
            executer.start_game(msg)
        elif msg["body"].lstrip("-+").isdigit():
            executer.process_response(msg)

def main():
    token = load_token()
    bot = Client(token)

    try:
        messages = bot.get_messages()
        message_loop(messages, bot)
    

    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print (e)

if __name__ == "__main__": main()