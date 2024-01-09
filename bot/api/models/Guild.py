from dataclasses import dataclass


@dataclass
class GuildDTO:
    id: int
    settings: dict


@dataclass
class GuildRequestRemote:
    id: int


def mapDictToGuild(obj: dict) -> GuildDTO | None:
    return GuildDTO(**obj)
