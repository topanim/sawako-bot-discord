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
class UpdatedMemberReceiveRemote:
    before: MemberDTO
    after: MemberDTO


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


@dataclass
class UpdateMemberExpRequestRemote:
    guild_id: int
    user_id: int
    quantity: int


def mapDictToUpdatedMember(obj: dict) -> UpdatedMemberReceiveRemote | None:
    return UpdatedMemberReceiveRemote(
        before=MemberDTO(**obj['before']),
        after=MemberDTO(**obj['after']))


def mapDictToMember(obj: dict) -> MemberDTO | None:
    return MemberDTO(**obj)
