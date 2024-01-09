from disnake import Embed


def SuccessEmbed(text: str):
    return Embed(title='Успешно', description=f'**Результат**: {text}')
