from disnake.ext import tasks
from disnake.ext.commands import Cog

from bot.api.SawakoAPI import sawako_api
from bot.utils.logging.Log import Log
from res.cache.guilds import guilds_cache

logger = Log(__file__)


class CacheControl(Cog):
    def __init__(self):
        self.update_cache.start()

    def cog_unload(self) -> None:
        self.update_cache.stop()

    @tasks.loop(minutes=1.0)
    async def update_cache(self):
        logger.i('Update guilds cache')
        guilds = sawako_api.fetch_guilds()
        for guild in guilds:
            guilds_cache[guild.id] = guild.settings
