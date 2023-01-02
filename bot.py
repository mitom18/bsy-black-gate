import requests
import os
import sys
from dotenv import load_dotenv


class Bot:
    def __init__(self, gist_id, name):
        self.gist_id = gist_id
        self.name = name
        self.current_bot = None
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + os.getenv("GITHUB_API_TOKEN"),
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def run(self):
        print("Running as %s" % self.name)
        exit()


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
