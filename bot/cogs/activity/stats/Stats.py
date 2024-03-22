from disnake import Embed
from disnake.ext.commands import Cog, Bot, slash_command

from bot.api.SawakoAPI import sawako_api
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.logging.Logger import Logger

logger = Logger(__file__)


class Stats(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot

    @slash_command(description='Таблица лидеров')
    async def leaders(self, inter):
        await inter.response.defer()

        users = sawako_api.fetch_members_top(inter.guild.id)
        embed = Embed(title='Таблица лидеров', description=inter.guild) \
            .set_thumbnail(url=inter.guild.icon.url)

        top = 1
        for user in users[:10]:  # TODO: Create Pagination
            member = inter.guild.get_member(user.user_id)
            embed.add_field(name=f'#{top} {member.display_name}',
                            value=f'lvl `{user.lvl}` | exp `{user.exp}/{user.up_exp}`',
                            inline=False)
            top += 1
        await inter.base_send(embed=embed, ephemeral=True)
