COMMAND_HELP = {"name": "help", "description": "Prints all the available commands."}
COMMAND_BOT = {"name": "bot", "description": "Switch the currently controlled bot."}
COMMAND_USERS = {
    "name": "users",
    "description": "List all active users on the bot.",
    "command": "Could you send me list of users?",
}
COMMAND_EXIT = {"name": "exit", "description": "Exit from the application."}

COMMANDS_CONTROLLER = [COMMAND_HELP, COMMAND_BOT, COMMAND_USERS, COMMAND_EXIT]

COMMANDS_BOT = {COMMAND_USERS["command"]: COMMAND_USERS}
