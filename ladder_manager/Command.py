from enum import Enum, auto

class Command(Enum):
    cancel = auto()
    help = auto()
    board = auto()
    not_a_command = auto()
    report = auto()
    teams = auto()
    set = auto()
    unknown = auto()
    #update_admins = auto()