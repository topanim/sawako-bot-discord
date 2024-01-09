from disnake import Member
from disnake.ext.commands import Cog, Bot

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Member import MemberRequestRemote
from bot.cogs.logging.base.ui.JoinRemoveEmbed import JoinRemoveEmbed
from bot.api.cache.guilds import guilds_cache
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.event_dispatcher.Dispatcher import Dispatcher
from bot.utils.logging.Log import Log

logger = Log(__file__)


class MemberJoinRemove(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot

    @Cog.listener("on_member_join")
    async def on_member_join(self, member: Member):
        if member.bot:
            return

        settings = guilds_cache[member.guild.id]['settings']
        if settings['greeting']['enabled'] and settings['greeting']['channel']:
            greeting_channel = self.bot.get_channel(settings['greeting']['channel'])

            await Dispatcher.dispatch(
                channel=greeting_channel,
                send_obj=settings['greeting']['send'],
                data={
                    'guild': member.guild,
                    'member': member,
                }
            )

        if settings['logging']['enabled'] and settings['logging']['channel']:
            logs_channel = self.bot.get_channel(settings['logging']['channel'])
            embed = JoinRemoveEmbed(member=member, action='присоединился')
            await logs_channel.send(embed=embed)

    @Cog.listener("on_member_remove")
    async def on_member_remove(self, member: Member):
        if member.bot:
            return

        sawako_api.delete_member(MemberRequestRemote(member.guild.id, member.id))
        settings = guilds_cache[member.guild.id]['settings']['logging']

        if settings['enabled'] and settings['channel']:
            channel = self.bot.get_channel(settings['channel'])
            embed = JoinRemoveEmbed(member=member, action='вышел')
            await channel.send(embed=embed)
