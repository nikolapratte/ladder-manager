import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


def get_token():
    """Gets the Discord bot token from the assumed filename.

    File should just be the token, no other characters."""
    token_filename = "token.txt"

    with open(token_filename) as f:
        return f.read()


if __name__ == "__main__":

    client = MyClient()
    client.run(get_token())