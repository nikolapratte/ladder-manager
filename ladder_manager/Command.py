from enum import Enum, auto

class Command(Enum):
    help = auto()
    report = auto()
    unknown = auto()