from .CommandInformation import CommandInformation, ReportInformation
import asyncio
from typing import List, Optional, Tuple

import discord

from .Command import Command
from .constants import cancel_emoji, command_descriptions, command_names, command_symbol, command_to_information, \
debug, delete_msgs_after, main_ladder_name, timeout_limit, timeout_message
from .LadderDB import LadderDB


def parse_message(message: discord.Message) -> Optional[Command]:
    msg_str: str = message.content
    msg_str = msg_str.lower()

    if not msg_str.startswith(command_symbol):
        return Command.not_a_command

    # recognize each command by their name
    for command, command_name in command_names.items():
        command: Command
        command_name: str
        if msg_str.startswith(f"{command_symbol}{command_name.lower()}"):
            return command


class MyClient(discord.Client):
    """Queue of messages to send out. Cleared on every message sent."""
    def __init__(self):
        self.users_running_commands = set()
        super().__init__()

    async def process_message_dm(self, message: discord.Message) -> None:
        await self.send(message.channel,
        f"Hello {message.author}, I do not take DMs at the moment.")
        

    async def send(self, channel: discord.abc.Messageable, message: str, delete_after: float = None) -> discord.Message:
        """Sends a Discord message."""
        return await channel.send(message, delete_after = delete_after)

    async def menu(self, message: discord.Message, user_target: discord.User, options: List[str]) -> Optional[str]:
        """Creates a menu out of the given message.
        
        Expects the given user to react with one of the
        given options (which are unicode emojis).
        
        Returns either the emoji the user chose or None, which means they timed out or chose the cancel option."""
        options.append(cancel_emoji)

        # check if user reacted with one of the appropriate emojis
        def check(reaction: discord.Reaction, user: discord.User) -> bool:
            return user == user_target and str(reaction.emoji) in options

        # put out messages and reactions on them so user can just click the reactions
        for emoji in options:
            await message.add_reaction(emoji)

        try:
            reaction, user = await self.wait_for("reaction_add", timeout=timeout_limit, check=check)

            if reaction.emoji == cancel_emoji:
                return

            #await asyncio.gather(*[message.remove_reaction(emoji, self.user) for emoji in options])
            for emoji in options:
                asyncio.create_task(message.remove_reaction(emoji, self.user))
            return reaction.emoji
        except asyncio.TimeoutError:
            return

    
    def get_db(self, ladder_name: str) -> LadderDB:
        """Retrieves the db for the given ladder name. Putting this in a function
        allows for caching or other special things later on."""
        return LadderDB(ladder_name)


    async def run_command(self, ladder_name: str, channel: discord.abc.Messageable,
     command: Command, info: CommandInformation = None) -> None:
        """Runs the given command.
        
        Will raise a ValueError if not provided enough information for a command
        that needs information."""
        assert ladder_name is not None
        assert command is not None


        if command is Command.help:
            output = ""
            for command, name in command_names.items():
                output += f"{name}: {command_descriptions[command]}\n"

            await self.send(channel, output)
        elif command is Command.leaderboard:
            db = self.get_db(ladder_name)
            output = "LEADERBOARD"

            board = db.leaderboard()
            print(board)
            for user_id, rating in board:
                output += f"{self.get_user(user_id)}\t{rating}\n"

            await self.send(channel, output)
        elif command is Command.report:
            if info is None:
                raise ValueError("[info] should not be None for a command that requires [info].")
            # Retype info as a [ReportInformation] now that it is known the command is for Report
            info: ReportInformation = info

            # backend stuff
            db = self.get_db(ladder_name)
            
            p1 = info.user.id
            p2 = info.opponent.id
            p1_starting_mmr = db.get_player_rating(p1) if db.player_exists(p1) else LadderDB.starting_rating
            p2_starting_mmr = db.get_player_rating(p2) if db.player_exists(p2) else LadderDB.starting_rating

            p1_new_mmr, p2_new_mmr = db.process_match(p1, p2, info.match_history)

            # update users on rating changes

            await self.send(channel, f"""{info.user.display_name}'s rating went from {p1_starting_mmr} to {p1_new_mmr}.
{info.opponent.display_name}'s rating went from {p2_starting_mmr} to {p2_new_mmr}""")


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

            # list of game score messages (need for id to delete later on)
            game_score_msgs = list()


            # put out messages and reactions on them so user can just click the reactions
            while True:
                game_score_msg: discord.Message = await self.send(channel, f"Who won game {len(match_history) + 1}?")
                game_score_msgs.append(game_score_msg)

                choice = await self.menu(game_score_msg, message.author, ["👍", "👎", "🆗"])
                
                if choice is None:
                    await self.send(message.channel, timeout_message)
                    # clean up messages to avoid spam
                    for bot_message in game_score_msgs:
                        await bot_message.delete()
                    return

                if choice == "👍":
                    match_history += "1"
                elif choice == "👎":
                    match_history += "0"
                elif choice == "🆗":
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
                return mention_message.author == message.author and len(mention_message.mentions) != 0

            # repeat asking for user mentions until user mentions only 1 user.
            while True:
                try:
                    mention_msg: discord.Message = await self.wait_for("message", timeout=timeout_limit, check=check)
                    if debug:
                        print(f"Recognizing mention message as: {mention_msg.content}")
                except asyncio.TimeoutError:
                    await self.send(channel, timeout_message)
                    return
                # TODO should also make sure user isn't pinging self, or bots
                if len(mention_msg.mentions) == 1:
                    break
                await self.send(mention_msg.channel, "Only mention 1 user.", delete_after = delete_msgs_after)
            
            opponent_name = mention_msg.mentions[0].display_name
            await explanation_msg.edit(content = f"{explanation_start}{opponent_name} needs to verify match. 👍 to verify, {cancel_emoji} to cancel.", )

            choice = await self.menu(explanation_msg, mention_msg.mentions[0], ["👍"])
            if choice is None:
                await explanation_msg.edit(content = f"{opponent_name} did not verify before timeout, match report cancelled.",
                delete_after = delete_msgs_after)
                return

            await explanation_msg.edit(content = "Match processing...", delete_after = delete_msgs_after)

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
            return
        else:
            command: Command = parse_message(message)

        # if no command matched, end
        if command is Command.not_a_command:
            return
        elif message.author in self.users_running_commands:
            if command is Command.cancel:
                # TODO actual cancel by holding await object and referencing and cancelling it.
                await self.send(message.channel, "Please wait until your last command times out, or type invalid input.")
            else:
                await self.send(message.channel, "You can only have one command running at a time.")
            return
        elif command is None:
            await self.send(message.channel, "Sorry, I don't recognize that.", delete_after = delete_msgs_after)
            return
        else:
            # otherwise, add user to commands list since only one command can be run for a user at a time
            self.users_running_commands.add(message.author)

        # FUTURE decide where command should go based on guild, settings, channel, etc.
        # load up appropriate database
        ladder_name = main_ladder_name

        if command_to_information[command] is not None:
            info: CommandInformation = await self.get_information(command, message)
            # if did not get information, skip past running command and go to cleanup section
            if info is not None:
                await self.run_command(ladder_name, message.channel, command, info)
        else:
            await self.run_command(ladder_name, message.channel, command)

        # once done running, take user out of users running commands
        # TODO may be better to use environment (with) to ensure this is run.

        self.users_running_commands.remove(message.author)