from colorama import Fore
from discord.utils.Insert import insert_guild
from disnake.ext.commands import Cog, Bot

from api.SawakoAPI import sawako_api
from api.models.Guild import GuildRequestRemote


class Start(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def start_log(self):
        print(Fore.GREEN + f"Logged in as {self.bot.user} (ID: {self.bot.user.id})\n------")

    @Cog.listener("on_ready")
    async def add_persistent_views(self):
        # self.add_view()
        pass

    @Cog.listener("on_ready")
    async def create_models(self):
        for guildDTO in sawako_api.fetch_guilds():

            guild = self.bot.get_guild(guildDTO.id)

            if not guild:
                sawako_api.delete_guild(GuildRequestRemote(guildDTO.id))
                continue

            for memberDTO in sawako_api.fetch_members_from_guild(guildDTO.id):
                member = guild.get_member(memberDTO.user_id)

                if not member:
                    sawako_api.delete_member(memberDTO.id)

        for guild in self.bot.guilds:
            insert_guild(guild)
