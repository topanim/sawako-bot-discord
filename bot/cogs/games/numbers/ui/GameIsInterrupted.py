from disnake import Embed


def GameIsInterrupted(player: str):
    return Embed(title="Игра была прервана", description=f"{player} прервал игру")
