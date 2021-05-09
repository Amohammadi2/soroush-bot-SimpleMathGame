from client import Client 
from token_loader import load_token

def main():
    token = load_token()
    bot = Client(token)
    try:
        messages = bot.get_messages()
        for message in messages:
            print (message)
            message["to"] = message["from"]
            message.pop("from")
            message.pop("time")
            bot.send_message(message)
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print (e)

if __name__ == "__main__": main()