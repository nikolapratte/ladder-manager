
from .Command import Command

class HelpDatum:
    """Provides data meant to be shown to users on help pages."""
    def __init__(self):
        pass

# information on each command
help_data = {
    Command.report : HelpDatum()
}