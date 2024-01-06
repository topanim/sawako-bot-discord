from dataclasses import asdict

from requests import get, post

from api.models.Guild import GuildRequestRemote, mapDictToGuild, GuildDTO
from api.models.Member import MemberRequestRemote, mapDictToMember, MemberDTO
from api.models.User import UserRequestRemote, mapDictToUser, UserDTO


class SawakoAPI:
    # base
    BASE_URL = "http://127.0.0.1:8080/"

    # users
    USERS_CREATE = BASE_URL + "users/create"
    USERS_FETCH_ALL = BASE_URL + "users/"
    USERS_FETCH_ONE = BASE_URL + "users/{id}"
    USERS_DELETE = BASE_URL + "users/{id}"

    # guilds
    GUILDS_CREATE = BASE_URL + "guilds/create"
    GUILDS_FETCH_ALL = BASE_URL + "guilds/"
    GUILDS_FETCH_ONE = BASE_URL + "guilds/{id}"
    GUILDS_DELETE = BASE_URL + "guilds/{id}/delete"

    # members
    MEMBERS_CREATE = BASE_URL + "members/create"
    MEMBERS_FETCH_ALL_FROM_GUILD = BASE_URL + "members/from/{id}"
    MEMBERS_FETCH_TOP = BASE_URL + "members/top?guild_id={id}"
    MEMBERS_FETCH_ALL = BASE_URL + "members/"
    MEMBERS_FETCH_ONE = BASE_URL + "members/one/?guild_id={guild_id}&user_id={user_id}"
    MEMBERS_DELETE = BASE_URL + "members/{id}/delete"

    @staticmethod
    def create_user(user: UserRequestRemote):
        return post(SawakoAPI.USERS_CREATE, json=asdict(user))

    @staticmethod
    def fetch_user(user_id: int):
        return mapDictToUser(get(SawakoAPI.USERS_FETCH_ONE.format(id=user_id)).json())

    @staticmethod
    def fetch_users():
        return list(map(lambda it: mapDictToUser(it), get(SawakoAPI.USERS_FETCH_ALL).json()))

    @staticmethod
    def delete_user(user: UserDTO):
        return post(SawakoAPI.USERS_DELETE.format(id=user.id))

    @staticmethod
    def create_guild(guild: GuildRequestRemote):
        return post(SawakoAPI.GUILDS_CREATE, json=asdict(guild))

    @staticmethod
    def fetch_guild(guild_id: int):
        return mapDictToGuild(get(SawakoAPI.GUILDS_FETCH_ONE.format(id=guild_id)).json())

    @staticmethod
    def fetch_guilds():
        return list(map(lambda it: mapDictToGuild(it), get(SawakoAPI.GUILDS_FETCH_ALL).json()))

    @staticmethod
    def delete_guild(guild: GuildDTO):
        return post(SawakoAPI.USERS_DELETE.format(id=guild.id))

    @staticmethod
    def create_member(member: MemberRequestRemote):
        print(asdict(member))

        return post(SawakoAPI.MEMBERS_CREATE, json=asdict(member))

    @staticmethod
    def fetch_member(guild_id: int, user_id: int):
        return mapDictToMember(get(
            SawakoAPI.MEMBERS_FETCH_ONE.format(guild_id=guild_id, user_id=user_id)
        ).json())

    @staticmethod
    def fetch_members():
        return list(map(lambda it: mapDictToMember(it), get(SawakoAPI.MEMBERS_FETCH_ALL).json()))

    @staticmethod
    def fetch_members_top(guild):
        return list(map(lambda it: mapDictToMember(it),
                        get(SawakoAPI.MEMBERS_FETCH_TOP.format(id=guild)).json()))

    @staticmethod
    def fetch_members_from_guild(guild: int):
        return list(map(lambda it: mapDictToMember(it),
                        get(SawakoAPI.MEMBERS_FETCH_ALL_FROM_GUILD.format(id=guild)).json()))

    @staticmethod
    def delete_member(member: MemberDTO):
        return post(SawakoAPI.USERS_DELETE.format(id=member.id))


sawako_api = SawakoAPI()
