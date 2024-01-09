from datetime import datetime

from disnake import Guild, Member, Embed

from bot.api.models.Member import MemberDTO


def ProfileEmbed(guild: Guild, user: Member, dto: MemberDTO):
    embed = Embed(title=f'Профиль {user.display_name}', timestamp=datetime.now())
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_footer(icon_url=user.avatar.url, text=f'ID: {user.id}')
    else:
        embed.set_thumbnail(url=user.default_avatar.url)
        embed.set_footer(icon_url=user.default_avatar.url, text=f'ID: {user.id}')
    embed.add_field(name='Имя', value=f'`{dto.name}`') \
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
