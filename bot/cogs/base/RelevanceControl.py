import disnake
from disnake.ext.commands import Cog, Bot

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Member import MemberRequestRemote
from bot.utils.database.insert import insert_guild
from bot.utils.logging.Log import Log
from bot.utils.logging.decorators.on_use import on_use

logger = Log(__file__)


class RelevanceControl(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_guild_join")
    async def add_guild(self, guild: disnake.Guild):
        logger.i(f'Insert guild - {guild.name}')
        insert_guild(guild)

    @Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: disnake.Guild):
        logger.i(f'Delete guild - {guild.name}')
        sawako_api.delete_guild(guild.id)

    @Cog.listener("on_member_join")
    async def on_member_join(self, member: disnake.Member):
        if not member.bot:
            logger.i(f'Insert member - {member.name}')
            sawako_api.create_member(MemberRequestRemote(member.guild.id, member.id))

    @Cog.listener("on_member_remove")
    async def on_member_remove(self, member: disnake.Member):
        if not member.bot:
            logger.i(f'Delete member - {member.name}')
            sawako_api.delete_member(member.guild.id, member.id)
