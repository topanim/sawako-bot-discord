from os import getenv

from disnake import Intents, ActivityType, Activity
from disnake.ext import commands
from dotenv import load_dotenv

from bot.cogs.activity.profile.Profile import Profile
from bot.cogs.activity.stats.Stats import Stats
from bot.cogs.base.CacheControl import CacheControl
from bot.cogs.base.RelevanceControl import RelevanceControl
from bot.cogs.base.Start import Start
from bot.cogs.games.numbers.Numbers import Numbers
from bot.utils.logging.Log import Log

load_dotenv()

logger = Log(__file__)


def main():
    client = commands.Bot(
        command_prefix="!",
        intents=Intents.all(),
        help_command=None,
        activity=Activity(name="за своими котятами", type=ActivityType.watching),
    )

    # Base
    client.add_cog(Start(client))
    client.add_cog(RelevanceControl(client))
    client.add_cog(CacheControl())

    # Activity
    client.add_cog(Profile(client))
    client.add_cog(Stats(client))

    # Games
    client.add_cog(Numbers(client))

    client.run(getenv("BOT_TOKEN"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.i('Log out!')
