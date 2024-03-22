from datetime import datetime

from disnake import Embed

from res.colors.Color import Color


def MemberUpdateEmbed(entry, action: str, color: int):
    return Embed(title=action, color=color, timestamp=datetime.now()) \
        .add_field(name='Пользователь', value=f'```fix\n{entry.target}```') \
        .add_field(name='Модератор', value=f'```fix\n{entry.user}```') \
        .add_field(name='Причина', value=f'```py\n{entry.reason if entry.reason else "Отсутствует"}```', inline=False) \
        .set_footer(text=f'ID: {entry.target.id}') \
        .set_thumbnail(url=entry.target.avatar.url)

