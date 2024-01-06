from dataclasses import dataclass


@dataclass
class MemberDTO:
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


def mapDictToMember(obj: dict) -> MemberDTO | None:
    # try:
        return MemberDTO(**obj)
    # except:
    #     return
