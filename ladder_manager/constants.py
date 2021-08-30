"""Filename of a text file containing only the bot's Discord token.

File should not contain any extra characters."""

from .Command import Command
from .CommandInformation import CommandInformation, ReportInformation



command_names = {Command.help: "Help",
    Command.report: "Report"}

# Mapping between commands and what information they need.
# If a command doesn't need extra information, will have None.
command_to_information = {Command.report: ReportInformation}
command_symbol = "!"

delete_msgs_after = 10

# will be deprecated once do db per server/channel.
main_ladder_name = "main_ladder.db"

timeout_message = "Sorry, your session timed out. Please try again."
timeout_limit = 15
token_filename = "ladder_manager/token.txt"


# dev constants

debug = True
test_db_filename = "test.db"

