
from constants import token_filename
from MyClient import MyClient


def get_token(token_filename: str) -> None:
    """Gets the Discord bot token from the given filename.

    File should just be the token, no other characters."""
    with open(token_filename) as f:
        return f.read()


if __name__ == "__main__":

    client = MyClient()
    client.run(get_token(token_filename))