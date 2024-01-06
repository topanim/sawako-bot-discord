from datetime import datetime

from disnake import Embed, Member, Guild, ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Cog, Bot

from api.SawakoAPI import sawako_api
from api.models.Member import MemberDTO


class Stats(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @classmethod
    def create_profile_embed(cls, *, guild: Guild, user: Member, dto: MemberDTO):
        embed = Embed(title=f'Профиль {user.display_name}', timestamp=datetime.now())
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
            embed.set_footer(icon_url=user.avatar.url, text=f'ID: {user.id}')
        else:
            embed.set_thumbnail(url=user.default_avatar.url)
            embed.set_footer(icon_url=user.default_avatar.url, text=f'ID: {user.id}')
        embed.add_field(name='Имя', value=f'`{user.display_name}`') \
            .add_field(name='День рождения', value=f'`{dto.birthdate}`') \
            .add_field(name='Пол', value=f'`{dto.gender}`') \
            .add_field(name='Обо мне', value=f'```{dto.about}```', inline=False)
        if dto.lover:
            lover = guild.get_member(dto.lover)
            embed.add_field(name='Пара', value=lover.mention)
        else:
            embed.add_field(name='Пара', value='`Не в браке`')
        embed.add_field(name='Валюта', value=f'{dto.wallet} $') \
            .add_field(name='Уровень', value=f'{dto.lvl}\n`[{dto.exp}/{dto.up_exp}]`')

        return embed

    @commands.slash_command(description='Профиль')
    async def profile(
        self, inter: ApplicationCommandInteraction,
        user: Member = commands.Param(name='пользователь', default=None)
    ):
        await inter.response.defer()

        if not user:
            user = inter.author

        if user.bot:
            embed = Embed(title='Ошибка', description='**Заметка**: Боты не заносятся в базу')
            await inter.send(embed=embed, ephemeral=True)

        dto = sawako_api.fetch_member(guild_id=inter.guild.id, user_id=user.id)

        await inter.send(embed=self.create_profile_embed(
            guild=inter.guild,
            user=user,
            dto=dto
        ))

        # TODO: Create Button & Edit Modal
        # message = await inter.original_response()
        # await message.edit(view=SetprofileButton(user, message))

    @commands.slash_command(description='Таблица лидеров')
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
        await inter.send(embed=embed, ephemeral=True)
