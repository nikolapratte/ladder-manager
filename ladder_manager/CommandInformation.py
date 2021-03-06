from abc import ABC
from .constants import Command
from typing import List

import discord

class CommandInformation(ABC):
    """Abstract base class for classes that hold the necessary information
    to run a [Command]."""
    pass


class ReportInformation(CommandInformation):
    def __init__(self, match_history: str, user: discord.Member, opponent: discord.Member):
        assert isinstance(match_history, str)
        assert isinstance(user, discord.Member)
        assert isinstance(opponent, discord.Member)
        self.match_history = match_history
        self.user = user
        self.opponent = opponent


class SetInformation(CommandInformation):
    def __init__(self, user_id: int, rating: int) -> None:
        self.user_id = user_id
        self.rating = rating

    
class TeamsInformation(CommandInformation):
    def __init__(self, user_team: List[discord.Member], opponent_team: List[discord.Member], matches: str) -> None:
        self.user_team = user_team
        self.opponent_team = opponent_team
        self.matches = matches