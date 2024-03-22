from disnake import Member, ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Cog, Bot, slash_command

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Member import MemberRequestRemote
from bot.cogs.activity.profile.ui.ProfileEditButtons import ProfileEditButtons
from bot.cogs.activity.profile.ui.ProfileEmbed import ProfileEmbed
from bot.ui.embeds.ErrorEmbed import ErrorEmbed
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.logging.Logger import Logger

logger = Logger(__file__)


class Profile(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot

    @slash_command(description='Профиль')
    async def profile(
            self, inter: ApplicationCommandInteraction,
            user: Member = commands.Param(name='пользователь', default=None)
    ):
        await inter.response.defer()

        if not user:
            user = inter.author

        if user.bot:
            embed = ErrorEmbed('Боты не заносятся в базу')
            await inter.send(embed=embed, ephemeral=True)

        dto = sawako_api.fetch_member(MemberRequestRemote(guild_id=inter.guild.id, user_id=user.id))

        await inter.send(embed=ProfileEmbed(
            guild=inter.guild,
            user=user,
            dto=dto
        ))

        message = await inter.original_response()
        await message.edit(view=ProfileEditButtons(user, message))
