from disnake import Message, Embed
from disnake.ext.commands import Bot, Cog

from bot.api.cache.guilds import guilds_cache
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.event_dispatcher.Dispatcher import Dispatcher
from bot.utils.logging.Logger import Logger

logger = Logger(__file__)


class AutoMod(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot

    @Cog.listener('on_message')
    async def anti_caps(self, message: Message):
        await self.bot.process_commands(message)

        settings = guilds_cache[message.guild.id]['settings']['auto_mod']['anti_caps']
        temporary = message.content.upper()
        symbols = '0123456789@#$&-+()/*":;!?][^~`\' '
        count = 0

        for i in range(len(temporary)):
            if message.content[i] == temporary[i] and temporary[i] not in symbols:
                count += 1

        if count >= len(temporary) // 2 and len(temporary) >= 10:
            await message.delete()
            info_message = await Dispatcher.dispatch(
                channel=message.channel,
                send_obj=settings['send'],
                data={
                    'guild': message.guild,
                    'member': message.author,
                }
            )

            if settings['send']['auto_delete']:
                try:
                    await info_message.delete(defer=10)
                except:
                    return
