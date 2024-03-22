from disnake import Embed, Member, User


def LvlUpEmbed(user: User | Member, lvl: int):
    return Embed(title='Повышение уровня',
                 description=f'{user.mention} Ваш текущий уровень `{lvl}`') \
        .set_thumbnail(url=user.avatar.url)
