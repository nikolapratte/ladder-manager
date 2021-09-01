from enum import Enum, auto

class Command(Enum):
    cancel = auto()
    help = auto()
    leaderboard = auto()
    not_a_command = auto()
    report = auto()
    set = auto()
    unknown = auto()
    #update_admins = auto()