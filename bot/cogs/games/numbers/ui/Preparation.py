from disnake import Embed


def Preparation(player: str, icon_url: str):
    return Embed(title="Подготовка",
                 description=f"```py\n{player} Введите свое число, предворительно занеся его "
                             f"под спойлер\nПример - ||1234||```").set_footer(
                 text="Перед началом игры, ознакомьтесь с ее правилами /numbers rules",
                 icon_url=icon_url)
