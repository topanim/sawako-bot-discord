from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int


@dataclass
class UserRequestRemote:
    id: int


def mapDictToUser(obj: dict) -> UserDTO | None:
    try:
        return UserDTO(**obj)
    except:
        return
