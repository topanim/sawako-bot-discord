from dataclasses import dataclass
from json import loads


@dataclass
class User:
    id: int


@dataclass
class UserRequestRemote:
    id: int


def mapDictToUser(obj: dict) -> User | None:
    try:
        return User(**obj)
    except:
        return
