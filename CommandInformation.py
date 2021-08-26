from abc import ABC
from typing import List

import discord

class CommandInformation(ABC):
    """Abstract base class for classes that hold the necessary information
    to run a [Command]."""
    pass


class ReportInformation(CommandInformation):
    def __init__(self, match_history: List[int], user: discord.Member, opponent: discord.Member):
        self.match_history = match_history
        self.user = user
        self.opponent = opponent
