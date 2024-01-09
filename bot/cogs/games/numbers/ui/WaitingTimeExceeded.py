from disnake import Embed


def WaitingTimeExceededEmbed(player: str, minutes: str | int = 2):
    return Embed(title="Превышено время ожидания",
                 description=f"{player} не ответил в течении {minutes}х мин")
