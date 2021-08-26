"""Filename of a text file containing only the bot's Discord token.

File should not contain any extra characters."""

from Command import Command
from CommandInformation import CommandInformation, ReportInformation



command_names = {Command.report: "Report"}
command_to_information = {Command.report: ReportInformation}
command_symbol = "!"

debug = True
delete_msgs_after = 10

timeout_message = "Sorry, your session timed out. Please try again."
timeout_limit = 60
token_filename = "token.txt"

