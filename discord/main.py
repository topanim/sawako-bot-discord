import os

from disnake import Intents
from disnake.ext.commands import Bot, when_mentioned_or
from dotenv import load_dotenv

from bot.Client import Client

load_dotenv()


def main():
    client = Client(
        command_refix="!",
        intents=Intents.all()
    )

    client.run(os.getenv("BOT_TOKEN"))


if __name__ == "__main__":
    main()
