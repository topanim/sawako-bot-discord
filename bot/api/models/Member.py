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


@dataclass
class UpdateMemberBioRequestRemote:
    guild_id: int
    user_id: int
    name: str = None
    birthdate: str = None
    gender: str = None
    about: str = None


@dataclass
class UpdateMemberWalletRequestRemote:
    guild_id: int
    user_id: int
    amount: int


def mapDictToMember(obj: dict) -> MemberDTO | None:
    return MemberDTO(**obj)
