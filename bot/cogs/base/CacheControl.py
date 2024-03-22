from disnake.ext import tasks
from disnake.ext.commands import Cog

from bot.api.SawakoAPI import sawako_api
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.logging.Logger import Logger
from bot.api.cache.guilds import guilds_cache

logger = Logger(__file__)


class CacheControl(BaseCog):
    def __init__(self):
        super().__init__(logger)
        self.update_cache.start()

    def cog_unload(self) -> None:
        self.update_cache.stop()

    @tasks.loop(minutes=1.0)
    async def update_cache(self):
        logger.i('Update guilds cache')
        sawako_api.update_guilds_cache()
