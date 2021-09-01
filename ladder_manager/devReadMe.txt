To add a new command:

1. Add the command to [Command] enum, and
[command_names], [command_descriptions], and [command_to_information].
2. Add command to [admin_commands] if command is for admins.
3. If the command needs information from the user, add a clause to [get_information].
4. Add a clause to [run_command].