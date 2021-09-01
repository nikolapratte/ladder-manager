"""Filename of a text file containing only the bot's Discord token.

File should not contain any extra characters."""

from .Command import Command
from .CommandInformation import ReportInformation, SetInformation

admin_commands = set([Command.set])

cancel_emoji = "❌"

command_alternative_names = {
    Command.help: "h"
}

command_names = {
    Command.cancel: "Cancel",
    Command.help: "Help",
    Command.leaderboard: "Leaderboard",
    Command.report: "Report",
    Command.set: "Set",
    Command.update_admins: "update_admins"
    }

command_descriptions = {
    Command.cancel: "Cancels the current command.",
    Command.help: "List of commands and short descriptions of what they do.",
    Command.leaderboard: "Shows leaderboard of players",
    Command.report: "Report a match.",
    Command.set: "Set a player rating.",
    Command.update_admins: 'Adds all users with "Manage Server" permission to bot\'s admin list.'
}

# Mapping between commands and what information they need.
# If a command doesn't need extra information, will have None.
command_to_information = {
    Command.report: ReportInformation,
    Command.set: SetInformation,
    Command.help: None,
    Command.leaderboard: None,
    Command.update_admins: None
}
command_symbol = "!"

delete_msgs_after = 10

# will be deprecated once do db per server/channel.
main_ladder_name = "main_ladder.db"

timeout_message = "Sorry, your session was cancelled or timed out. Please try again."
timeout_limit = 15
token_filename = "ladder_manager/token.txt"


# dev constants

debug = True
test_db_filename = "test.db"
server_db_name = "ladder_server.db"
