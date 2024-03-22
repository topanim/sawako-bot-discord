from aiogram import Bot
from discord.ext.commands import has_permissions
from disnake import Member
from disnake.ext.commands import slash_command, Param

from bot.ui.embeds.ErrorEmbed import ErrorEmbed
from bot.ui.embeds.SuccessEmbed import SuccessEmbed
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.logging.Logger import Logger

logger = Logger(__file__)


class Moderation(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot

    # TODO: Add settings check permissions

    @slash_command()
    async def mod(self, inter):
        pass

    @mod.sub_command(description='Выгнать')
    async def kick(
            self,
            inter,
            member: Member = Param(name='пользователь'),
            reason: str = Param(name='причина', default='')
    ):
        embed = SuccessEmbed(f'Участник {member.mention} выгнан')
        await inter.base_send(embed=embed, ephemeral=True)
        await member.kick(reason=f"'Команда: {inter.author}'\n{reason}")

    @mod.sub_command(description='Выдать блокировку')
    async def ban(
            self,
            inter,
            member: Member = Param(name='пользователь'),
            reason: str = Param(name='причина', default=None)
    ):
        if member.bot:
            await inter.base_send(content="Вы не можете заблокировать бота!", ephemeral=True)

        embed = SuccessEmbed(f'Участнику {member.mention} выдана блокировка')
        await inter.base_send(embed=embed, ephemeral=True)
        await member.ban(reason=f"'Команда: {inter.author}'\n{reason}")

    @mod.sub_command(description='Снять блокировку')  # выдать таймаут пользователю
    async def unban(
            self,
            inter,
            user: Member = Param(name='пользователь'),
            reason: str = Param(name='причина', default='')
    ):
        embed = SuccessEmbed(f'С участника {user.mention} снята блокировка')
        await inter.base_send(embed=embed, ephemeral=True)
        await user.unban(reason=f"'Команда: {inter.author}'\n{reason}")

    @mod.sub_command(description='Выдать таймаут')
    async def mute(
            self,
            inter,
            user: Member,
            duration: str = Param(name='длительность', default='10m'),
            reason: str = Param(name='причина', default='')
    ):
        try:
            timedict = {'d': 86400, 'h': 3600, 'm': 60}
            count, time = duration[:-1], duration[-1]
            await user.timeout(reason=f"'Команда: {inter.author}'\n{reason}", duration=int(count) * timedict[time])
            embed = SuccessEmbed(f'Пользователю {user.mention} выдано заглушение')
            await inter.base_send(embed=embed, ephemeral=True)
        except AttributeError:
            embed = ErrorEmbed('Значения указаны неверно')
            await inter.base_send(embed=embed, ephemeral=True)

    @mod.sub_command(description='Вернуть голос')
    async def unmute(
            self,
            inter,
            user: Member = Param(name='пользователь'),
            reason: str = Param(name='причина', default='')
    ):
        await user.timeout(reason=f"'Команда: {inter.author}'\n{reason}", until=None)
        embed = SuccessEmbed(f'Пользователю {user.mention} возвращен голос')
        await inter.base_send(embed=embed, ephemeral=True)
