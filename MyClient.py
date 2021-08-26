import asyncio
from typing import List, Tuple

import discord

from Command import Command
from constants import timeout_message, debug


def parse_message(message: discord.Message) -> Command:
    return Command.report


class MyClient(discord.Client):
    """Queue of messages to send out. Cleared on every message sent."""

    async def process_message_dm(self, message: discord.Message) -> None:
        await self.send(message.channel,
        f"Hello {message.author}, I do not take DMs at the moment.")
        

    async def send(self, channel: discord.abc.Messageable, message: str) -> discord.Message:
        """Sends a Discord message."""
        return await channel.send(message)


    async def get_information(self, command: Command, message: discord.Message) -> None:
        """Gets information for the provided command if extra information is needed
        (for example, report needs score, order of matches). Returns None for
        commands that do not need extra information (such as help)."""
        channel: discord.abc.Messageable = message.channel

        if command is Command.report:
            # for match history, "1" means win for the author, "0" means loss for the author
            # left most refers to most recent
            match_history = ""

            # explanation of the game reporting loop
            await self.send(channel, 
            f"Reporting match: Click on 👍 to report a win and 👎 to report a loss. Click 🆗 when you are done.")

            options = ["👍", "👎", "🆗"]

            # check if user reacted with one of the appropriate emojis
            def check(reaction: discord.Reaction, user) -> bool:
                return user == message.author and str(reaction.emoji) in options

            # put out messages and reactions on them so user can just click the reactions
            while True:
                game_score_msg: discord.Message = await self.send(channel, f"Who won game {len(match_history) + 1}?")


                for emoji in options:
                    await game_score_msg.add_reaction(emoji)

                try:
                    reaction, user = await self.wait_for("reaction_add", timeout=30, check=check)
                except asyncio.TimeoutError:
                    # TODO this needs to do some extra stuff to make sure program stops running the command
                    # maybe custom exception
                    await self.send(channel, timeout_message)
                    return

                reaction: discord.Reaction
                user: discord.User

                if reaction.emoji == "👍":
                    match_history += "1"
                elif reaction.emoji == "👎":
                    match_history += "0"
                elif reaction.emoji == "🆗":
                    break
                
            if debug:
                print(f"Match history recorded as: {match_history}.")
                
        
        # FUTURE may need this later on
        # put the reactions to wait for in this gather function
        # results = await asyncio.gather()


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))


    async def on_message(self, message: discord.Message) -> None:
        # ignore messages from self...
        if message.author == self.user:
            return

        print('Message from {0.author}: {0.content}'.format(message))

        # check if DM message or from a server
        if message.guild is None:
            await self.process_message_dm(message)
        else:
            command: Command = parse_message(message)

        # FUTURE decide where command should go based on guild, settings, channel, etc.
        # load up appropriate database

        # work with command now know its parsed

        # have view, model for commands.

        info = await self.get_information(command, message)