import os

from disnake import Intents
from disnake.ext import commands
from dotenv import load_dotenv

from cogs.activity.stats import Stats
from cogs.models_manager import ModelsManager

load_dotenv()


def main():

    client = commands.Bot(
        command_prefix="!",
        intents=Intents.all()
    )

    # client.add_cog(Start(client))
    client.add_cog(ModelsManager(client))
    client.add_cog(Stats(client))

    client.run(os.getenv("BOT_TOKEN"))


if __name__ == "__main__":
    main()
