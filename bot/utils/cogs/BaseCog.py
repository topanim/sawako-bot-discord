from disnake.ext.commands import Cog

from bot.utils.logging.Log import Log


class BaseCog(Cog):
    def __init__(self, logger: Log):
        self.logger = logger
        super().__init__()

    @Cog.listener('on_ready')
    async def on_ready(self):
        self.logger.i(f'Cog is loaded: {self.__cog_name__}')
