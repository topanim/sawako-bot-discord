from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int


@dataclass
class UserRequestRemote:
    id: int


def mapDictToUser(obj: dict) -> UserDTO | None:
    return UserDTO(**obj)
