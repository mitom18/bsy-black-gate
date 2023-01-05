COMMAND_HELP = {"name": "help", "description": "Prints all the available commands."}
COMMAND_BOT = {"name": "bot", "description": "Switch the currently controlled bot."}
COMMAND_PING = {"name": "ping", "description": "Pings the currently controlled bot.", "command": "👌"}
COMMAND_USERS = {
    "name": "w",
    "description": "List all active users on the bot.",
    "command": "✋",
}
COMMAND_DIRECTORY = {
    "name": "ls",
    "description": "List content of a specified directory on the bot.",
    "command": "📚",
}
COMMAND_ID = {
    "name": "id",
    "description": "Get current user's id on the bot.",
    "command": "💬",
}
COMMAND_COPY = {
    "name": "cp",
    "description": "Copy specified file from the bot to the controller.",
    "command": "📦",
}
COMMAND_RUN = {
    "name": "run",
    "description": "Execute specified binary on the bot.",
    "command": "🤞",
}
COMMAND_EXIT = {"name": "exit", "description": "Exit from the controller application."}

COMMANDS_CONTROLLER = [
    COMMAND_HELP,
    COMMAND_BOT,
    COMMAND_USERS,
    COMMAND_DIRECTORY,
    COMMAND_ID,
    COMMAND_COPY,
    COMMAND_RUN,
    COMMAND_EXIT,
]

COMMANDS_BOT = {
    COMMAND_PING["command"]: COMMAND_PING,
    COMMAND_USERS["command"]: COMMAND_USERS,
    COMMAND_DIRECTORY["command"]: COMMAND_DIRECTORY,
    COMMAND_ID["command"]: COMMAND_ID,
    COMMAND_COPY["command"]: COMMAND_COPY,
    COMMAND_RUN["command"]: COMMAND_RUN,
}
