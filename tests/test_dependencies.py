from ..ladder_manager.Command import Command
from ..ladder_manager.constants import command_descriptions, command_names, command_to_information

# ensure that commands have all the information they need
def test_command_variable_dependencies():
    for command in Command:
        if command in (Command.cancel, Command.not_a_command, Command.unknown):
            continue

        assert command in command_to_information
        assert command in command_names
        assert command in command_descriptions