from CommandInformation import CommandInformation, ReportInformation
import asyncio
from typing import List, Optional, Tuple

import discord

from Command import Command
from constants import command_names, command_symbol, debug, delete_msgs_after, timeout_limit, timeout_message


def parse_message(message: discord.Message) -> Command:
    msg_str: str = message.content
    msg_str = msg_str.lower()

    # recognize each command by their name
    for command, command_name in command_names.items():
        command: Command
        command_name: str
        if msg_str.startswith(f"{command_symbol}{command_name.lower()}"):
            return command


class MyClient(discord.Client):
    """Queue of messages to send out. Cleared on every message sent."""

    async def process_message_dm(self, message: discord.Message) -> None:
        await self.send(message.channel,
        f"Hello {message.author}, I do not take DMs at the moment.")
        

    async def send(self, channel: discord.abc.Messageable, message: str, delete_after: float = None) -> discord.Message:
        """Sends a Discord message."""
        return await channel.send(message, delete_after = delete_after)


    async def get_information(self, command: Command, message: discord.Message) -> Optional[CommandInformation]:
        """Gets information for the provided command if extra information is needed.

        For example, report needs score, order of matches.
        
        Returns None for commands that do not need extra information (such as help).
        If a command does need extra information, but this function fails to get it,
        the function will return None. Use [command_to_information] to see if
        a command needs extra information."""
        channel: discord.abc.Messageable = message.channel

        if command is Command.report:
            # for match history, "1" means win for the author, "0" means loss for the author
            # left most refers to most recent
            match_history = ""

            # explanation of the game reporting loop
            explanation_start = f"{command_names[Command.report]} for {message.author.display_name}: "
            explanation_msg = await self.send(channel, 
            f"{explanation_start}Click on 👍 to report a win and 👎 to report a loss. Click 🆗 when you are done.")

            # options the user has in the game reporting loop
            options = ["👍", "👎", "🆗"]

            # list of game score messages (need for id to delete later on)
            game_score_msgs = list()

            # check if user reacted with one of the appropriate emojis
            def check(reaction: discord.Reaction, user) -> bool:
                return user == message.author and str(reaction.emoji) in options

            # put out messages and reactions on them so user can just click the reactions
            while True:
                game_score_msg: discord.Message = await self.send(channel, f"Who won game {len(match_history) + 1}?")
                game_score_msgs.append(game_score_msg)

                for emoji in options:
                    await game_score_msg.add_reaction(emoji)

                try:
                    reaction, user = await self.wait_for("reaction_add", timeout=timeout_limit, check=check)
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

            await explanation_msg.edit(content = f"{explanation_start}Processing...")

            # clean up messages to avoid spam
            for bot_message in game_score_msgs:
                await bot_message.delete()

            # move on to asking user about opponent
            wins = match_history.count("1")
            losses = match_history.count("0")
            await explanation_msg.edit(content = f"{explanation_start}Recorded {wins} wins and {losses} losses. Please ping your opponent.")

            # wait for response

            # check if user reacted with one of the appropriate emojis
            def check(mention_message: discord.Message) -> bool:
                if debug:
                    print(f"Running check to see if user pinged opponent. Author is {mention_message.author}, mentions are {len(mention_message.mentions)}. {message.author}, {mention_message.author == message.author and len(mention_message.mentions) != 0}")
                return mention_message.author == message.author and len(mention_message.mentions) != 0

            # repeat asking for user mentions until user mentions only 1 user.
            while True:
                try:
                    mention_msg: discord.Message = await self.wait_for("message", timeout=timeout_limit, check=check)
                    if debug:
                        print(f"Recognizing mention message as: {mention_msg.content}")
                except asyncio.TimeoutError:
                    # TODO this needs to do some extra stuff to make sure program stops running the command
                    # maybe custom exception
                    await self.send(channel, timeout_message)
                    return
                # TODO should also make sure user isn't pinging self, or bots
                if len(mention_msg.mentions) == 1:
                    break
                await self.send(mention_msg.channel, "Only mention 1 user.", delete_after = delete_msgs_after)
            
            await explanation_msg.edit(content = f"{explanation_start}Processing match, opponent recognized as {mention_msg.mentions[0].display_name}", delete_after = delete_msgs_after)

            return ReportInformation(match_history, message.author, mention_msg.mentions[0])
                
        
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

        # check if DM message (or group chat) or from a server
        if message.guild is None:
            await self.process_message_dm(message)
        else:
            command: Command = parse_message(message)

        # FUTURE decide where command should go based on guild, settings, channel, etc.
        # load up appropriate database

        # work with command now know its parsed

        # have view, model for commands.

        info: CommandInformation = await self.get_information(command, message)