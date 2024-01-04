from json import loads
from dataclasses import dataclass


@dataclass
class Member:
    id: int
    guild_id: int
    user_id: int
    name: str
    gender: str
    birthdate: str
    about: str
    lover: int
    exp: int
    lvl: int
    up_exp: int
    wallet: int


@dataclass
class MemberRequestRemote:
    guild_id: int
    user_id: int


def mapDictToMember(obj: dict) -> Member | None:
    try:
        return Member(**obj)
    except:
        return
