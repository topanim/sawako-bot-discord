from disnake.ext.commands import Cog, Bot

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Guild import GuildRequestRemote
from bot.api.models.Member import MemberRequestRemote
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.database.insert import insert_guild
from bot.utils.logging.Log import Log

logger = Log(__file__)


class Start(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot

    @Cog.listener("on_ready")
    async def start_log(self):
        logger.i(f"Logged in as {self.bot.user}")

    @Cog.listener("on_ready")
    async def add_persistent_views(self):
        # self.add_view()
        pass

    @Cog.listener("on_ready")
    async def create_models(self):
        logger.i('Updating database')

        for guildDTO in sawako_api.fetch_guilds():

            guild = self.bot.get_guild(guildDTO.id)

            if not guild:
                sawako_api.delete_guild(GuildRequestRemote(guildDTO.id))
                continue

            for member_dto in sawako_api.fetch_members_from_guild(guildDTO.id):
                member = guild.get_member(member_dto.user_id)

                if not member:
                    sawako_api.delete_member(MemberRequestRemote(member_dto.user_id, member_dto.guild_id))

        for guild in self.bot.guilds:
            insert_guild(guild)
