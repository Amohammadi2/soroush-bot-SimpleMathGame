# first, create "token.txt" in the root folder
def load_token():
    with open("../token.txt", "r") as token_file:
        content = token_file.read()
    return content