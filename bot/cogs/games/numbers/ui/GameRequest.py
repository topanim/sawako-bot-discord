from textwrap import dedent

from disnake import Embed


def GameRequest(author: str, bet: str | int, with_zero: str, icon_url: str):
    return Embed(
        title="Запрос на игру",
        description=dedent(f"""
            {author} хочет сыграть с вами в Числа
            **Cтавка**: {bet}
            **Игра**: {with_zero}
        """)).set_footer(
            text="Перед началом игры, ознакомьтесь с ее правилами /numbers rules",
            icon_url=icon_url)
