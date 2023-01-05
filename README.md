# Command & Control

This project was done as a bonus task for BSY subject at FEE CTU. Bots and controller are communicating via GitHub Gist. Controller is sending commands to bots, bots are responding.

The communication functions as follows: Bot connects to the channel by creating a Markdown file with its name. Controller checks the markdown files and gets the bot names from the file names. Controller then sends commands to the bots using Gist comments. The comment starts with the bot's name and command as emoji separated by space. On next line, the comment contains a HTML comment with command arguments. The bot listens for comments starting with its name. When one is created, the bot then executes the given command. After executing the command, the bot sends the response by editing the comment with the executed command - it adds a checkmark emoji and a HTML comment with the output. The controller listens for changes of the created comment and reads the response from it.

The availability of all bots is checked by the controller after a response from selected bot is received.

## Requirements

 - Linux OS
 - Python 3.9

## Installation

Before running the application, you need to install some Python packages. You can install them via pip.

```
python -m pip install -r requirements.txt
```

After that you need to create `.env` configuration file from the provided `.env.template` file. Just copy the file, rename it and fill the configuration values.

## Usage

First, you need to run the controller, then run the bot with a name that is not used already.

```
python controller.py

python bot.py <name>
```

After that, you can select the bot to control on the controller by executing a `bot` command. Then you can command the bot with following commands.

 - `help` - Prints all the available commands.
 - `bot` - Switch the currently controlled bot.
 - `w` - List all active users on the bot.
 - `ls` - List content of a specified directory on the bot.
 - `id` - Get current user's id on the bot.
 - `cp` - Copy specified file from the bot to the controller.
 - `run` - Execute specified binary on the bot.
 - `exit` - Exit from the controller application.
