from colorama import Fore
from disnake.ext.commands import Cog, Bot

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Guild import GuildRequestRemote
from bot.utils.database.insert import insert_guild
from bot.utils.logging.Log import Log
from bot.utils.logging.decorators.on_use import on_use, async_on_use

logger = Log(__file__)


class Start(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def start_log(self):
        logger.i(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")

    @Cog.listener("on_ready")
    async def add_persistent_views(self):
        # self.add_view()
        pass

    @Cog.listener("on_ready")
    async def create_models(self):
        print('hello')
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
