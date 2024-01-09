from disnake import Embed


def ErrorEmbed(text: str):
    return Embed(
        title='Ошибка',
        description=f'**Заметка**: {text}')
