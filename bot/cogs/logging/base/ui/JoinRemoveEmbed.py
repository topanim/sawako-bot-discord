from datetime import datetime

import disnake
from disnake import Embed, Member

from res.colors.Color import Color


def JoinRemoveEmbed(member: Member, action: str):
    return Embed(title=f'Пользователь {action}', color=Color.PURPLE) \
        .add_field(name='Участник', value=f'```fix\n{member}```') \
        .add_field(name='Дата', value=disnake.utils.format_dt(datetime.now())) \
        .set_thumbnail(url=member.avatar)


