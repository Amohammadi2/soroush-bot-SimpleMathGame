from client import Client 
from token_loader import load_token

def main():
    token = load_token()
    print (token)
    bot = Client(token)
    try:
        messages = bot.get_messages()
        for message in messages:
            print (message)
    except Exception as e:
        print (e)

if __name__ == "__main__": main()