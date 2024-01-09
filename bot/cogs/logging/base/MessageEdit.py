from datetime import datetime

from disnake import Message, Embed
from disnake.ext.commands import Cog, Bot

from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.logging.Log import Log
from res.colors.Color import Color
from bot.api.cache.guilds import guilds_cache

logger = Log(__file__)


class MessageEdit(BaseCog):
    def __int__(self, bot: Bot):
        self.bot = bot
        super().__init__(logger)

    @Cog.listener("on_message")
    async def on_message(self, message: Message):
        pass

    @Cog.listener("on_message_edit")
    async def on_message_edit(self, before: Message, after: Message):
        settings = guilds_cache[after.guild.id]['settings']['logging']
        print(settings)

        if settings['enabled'] and settings['channel'] and before.content != after.content:
            channel = after.guild.get_channel(settings['channel'])
            embed = Embed(title='Изменене сообщения', color=Color.YELLOW, timestamp=datetime.now()) \
                .set_thumbnail(url=after.author.avatar.url) \
                .add_field(name='Автор', value=f'```fix\n{after.author}```') \
                .add_field(name='Канал', value=after.channel.mention) \
                .add_field(name='До', value=before.content, inline=False) \
                .add_field(name='После', value=after.content, inline=False) \
                .set_footer(text=after.id)
            await channel.send(embed=embed)
