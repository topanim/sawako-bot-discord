from random import choice

from disnake import Message, Embed
from disnake.ext.commands import Bot, Cog

from bot.api.SawakoAPI import sawako_api
from bot.api.cache.guilds import guilds_cache
from bot.api.models.Member import UpdateMemberExpRequestRemote
from bot.cogs.activity.receiving.ui.LvlUpEmbed import LvlUpEmbed
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.event_dispatcher.Dispatcher import Dispatcher
from bot.utils.logging.Logger import Logger

logger = Logger(__file__)


class ReceivingActivity(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot

    @Cog.listener('on_message')
    async def on_message(self, message: Message):
        await self.bot.process_commands(message)
        user = message.author

        if not user or user.bot or not message.guild:
            return

        guild_id = message.guild.id
        settings = guilds_cache[guild_id]['settings']['activity']

        if not settings['enabled']:
            return

        if settings['channel']:
            channel = settings['channel']
        else:
            channel = message.channel
        channel = self.bot.get_channel(channel)

        updated_member = sawako_api \
            .update_member_exp_add(UpdateMemberExpRequestRemote(
                guild_id=message.guild.id,
                user_id=user.id,
                quantity=choice([1, 2, 3, 4])))

        if updated_member.after.lvl - updated_member.before.lvl:
            info_message = await Dispatcher.dispatch(
                channel=channel,
                send_obj=settings['send'],
                data={
                    'guild': message.guild,
                    'member': message.author,
                    'dto': updated_member
                }
            )

            if settings['send']['auto_delete']:
                try:
                    await info_message.delete(delay=10.0)
                except:
                    return
