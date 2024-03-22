from datetime import datetime

from disnake import AuditLogAction
from disnake.ext.commands import Cog, Bot
from disnake.utils import format_dt

from bot.api.SawakoAPI import sawako_api
from bot.api.cache.guilds import guilds_cache
from bot.cogs.logging.moderation.ui.MemberUpdateEmbed import MemberUpdateEmbed
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.logging.Logger import Logger
from res.colors.Color import Color

logger = Logger(__file__)


class MemberUpdate(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot
        self.log_dict = {
            'ban': ['Блокировка выдана', Color.RED],
            'kick': ['Участник выгнан', Color.RED],
            'unban': ['Снятие блокировки', Color.GREEN]
        }

    @Cog.listener('on_member_update')
    async def on_member_update(self, before, after):
        settings = guilds_cache[after.guild.id]['settings']['logging']

        if settings['enabled'] and settings['channel']:
            if not before.current_timeout and after.current_timeout:
                entry = await after.guild.audit_logs(limit=1, action=AuditLogAction.member_update).flatten()
                entry = entry[0]
                embed = MemberUpdateEmbed(entry=entry, action='Таймаут', color=Color.RED) \
                    .add_field(name='Время', value=f'До {format_dt(after.current_timeout)}',
                               inline=False)

                channel = self.bot.get_channel(settings['channel'])
                await channel.send(embed=embed)

            elif before.current_timeout and not after.current_timeout:
                entry = await after.guild.audit_logs(limit=1, action=AuditLogAction.member_update).flatten()
                entry = entry[0]
                embed = MemberUpdateEmbed(entry=entry, action='Голос возвращен', color=Color.GREEN)
                channel = self.bot.get_channel(settings['channel'])
                await channel.send(embed=embed)

    @Cog.listener('on_audit_log_entry_create')
    async def on_audit_log_entry_create(self, entry):
        settings = guilds_cache[entry.guild.id]['settings']['logging']

        if settings['enabled'] and settings['channel']:
            if entry.action.name in self.log_dict.keys():
                embed = MemberUpdateEmbed(
                    entry=entry,
                    action=self.log_dict[entry.action.name][0],
                    color=self.log_dict[entry.action.name][1])

                channel = entry.guild.get_channel(settings['channel'])
                await channel.base_send(embed=embed)
