from dataclasses import dataclass
from json import loads


@dataclass
class Guild:
    id: int
    settings: dict


@dataclass
class GuildRequestRemote:
    id: int


def mapDictToGuild(obj: dict) -> Guild | None:
    try:
        return Guild(**obj)
    except:
        return
