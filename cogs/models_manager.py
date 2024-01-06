import disnake
from discord.utils.Insert import insert_guild
from disnake.ext.commands import Cog, Bot

from api.SawakoAPI import sawako_api


class ModelsManager(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_guild_join")
    async def add_guild(self, guild: disnake.Guild):
        insert_guild(guild)

    @Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: disnake.Guild):
        sawako_api.delete_guild(guild.id)

    @Cog.listener("on_member_join")
    async def on_member_join(self, member: disnake.Member):
        if not member.bot:
            sawako_api.create_member(member.guild.id, member.id)

    @Cog.listener("on_member_remove")
    async def on_member_remove(self, member: disnake.Member):
        if not member.bot:
            sawako_api.delete_member(member.guild.id, member.id)