import requests
import os
from dotenv import load_dotenv

COMMAND_HELP = "h"
COMMAND_SWITCH_BOT = "switch_bot"
COMMAND_EXIT = "exit"

COMMAND_DESCRIPTIONS = {
    COMMAND_HELP: "Prints all the available commands.",
    COMMAND_SWITCH_BOT: "Switch the currently controlled bot.",
    COMMAND_EXIT: "Exit from the application.",
}


class Controller:
    def __init__(self, gist_id):
        self.gist_id = gist_id
        self.current_bot = None
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + os.getenv("GITHUB_API_TOKEN"),
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def run(self):
        while True:
            command = input("Enter a command (h for help): ")
            if command == COMMAND_HELP:
                for key, value in COMMAND_DESCRIPTIONS.items():
                    print(key, value)
            elif command == COMMAND_SWITCH_BOT:
                bot_name = input("Enter a bot name: ")
                if self.bot_available(bot_name):
                    self.current_bot = bot_name
                    print("Switch to the bot: '" + bot_name + "'")
                else:
                    print("No such bot: '" + bot_name + "'")
            elif command == COMMAND_EXIT:
                print("Exiting...")
                break
            else:
                print("Unknown command")

    def bot_available(self, bot_name):
        res = requests.get(os.getenv("GITHUB_API_URL") + "gists/" + self.gist_id, headers=self.headers)
        if res.status_code == 200:
            return (bot_name + ".jpeg") in res.json()["files"]
        else:
            return False


def main():
    load_dotenv()
    controller = Controller(os.getenv("GIST_ID"))
    controller.run()


if __name__ == "__main__":
    main()
