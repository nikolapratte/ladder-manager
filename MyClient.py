from typing import List

import discord

from Command import Command

def parse_message(message: discord.Message) -> Command:
    pass


class QueuedMessage:
    def __init__(self, channel: discord.abc.Messageable, string: str) -> None:
        """Parameters:
        channel: [discord.abc.Channel] - some sort of channel.
        string: [str] - message to send."""
        self.channel = channel
        self.string = string


class MyClient(discord.Client):
    """Queue of messages to send out. Cleared on every message sent."""
    messages: List[QueuedMessage] = []

    @staticmethod
    def process_message_dm(message: discord.Message) -> None:
        MyClient.messages.append(
            QueuedMessage(message.channel, 
        f"Hello {message.author}, I do not take DMs at the moment.")
        )

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message) -> None:
        # ignore messages from self...
        if message.author == self.user:
            return

        print('Message from {0.author}: {0.content}'.format(message))

        # check if DM message or from a server
        if message.guild is None:
            MyClient.process_message_dm(message)
        else:
            command = parse_message(message)

        # send queued messages
        for queued_message in MyClient.messages:
            queued_message: QueuedMessage
            await queued_message.channel.send(queued_message.string)

        # clear queued messages
        MyClient.messages.clear()