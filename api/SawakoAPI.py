from dataclasses import asdict
from json import dumps

import requests
from requests import get, post

from api.models.Guild import GuildRequestRemote, mapDictToGuild, Guild
from api.models.Member import MemberRequestRemote, mapDictToMember, Member
from api.models.User import UserRequestRemote, mapDictToUser, User


class SawakoAPI:
    # base
    BASE_URL = "http://127.0.0.1:8080/"

    # users
    USERS_CREATE = BASE_URL + "users/create"
    USERS_CREATE_PACK = BASE_URL + "users/create/pack"
    USERS_FETCH_ALL = BASE_URL + "users/"
    USERS_FETCH_ONE = BASE_URL + "users/{id}"

    # guilds
    GUILDS_CREATE = BASE_URL + "guilds/create"
    GUILDS_CREATE_PACK = BASE_URL + "guilds/create/pack"
    GUILDS_FETCH_ONE = BASE_URL + "guilds/{id}"
    GUILDS_FETCH_ALL = BASE_URL + "guilds/"

    # members
    MEMBERS_CREATE = BASE_URL + "members/create"
    MEMBERS_CREATE_PACK = BASE_URL + "members/create/pack"
    MEMBERS_FETCH_ALL = BASE_URL + "members/"
    MEMBERS_FETCH_ONE = BASE_URL + "members/{id}"

    @staticmethod
    def create_user(user: UserRequestRemote):
        return post(SawakoAPI.USERS_CREATE, data=asdict(user))

    @staticmethod
    def create_users(users: list[UserRequestRemote]):
        return post(SawakoAPI.USERS_CREATE_PACK, data=list(map(lambda it: asdict(it), users)))

    @staticmethod
    def fetch_user(user: User):
        return mapDictToUser(get(SawakoAPI.USERS_FETCH_ONE.format(id=user.id)).json())

    @staticmethod
    def fetch_users():
        return list(map(lambda it: mapDictToUser(it), get(SawakoAPI.USERS_FETCH_ALL).json()))

    @staticmethod
    def create_guild(guild: GuildRequestRemote):
        return post(SawakoAPI.GUILDS_CREATE, data=asdict(guild))

    @staticmethod
    def create_guilds(guilds: list[GuildRequestRemote]):
        return post(SawakoAPI.GUILDS_CREATE_PACK, data=list(map(lambda it: asdict(it), guilds)))

    @staticmethod
    def fetch_guild(guild: Guild):
        return mapDictToGuild(get(SawakoAPI.GUILDS_FETCH_ONE.format(id=guild.id)).json())

    @staticmethod
    def fetch_guilds():
        return list(map(lambda it: mapDictToGuild(it), get(SawakoAPI.GUILDS_FETCH_ALL).json()))

    @staticmethod
    def create_member(guild: MemberRequestRemote):
        return post(SawakoAPI.MEMBERS_CREATE, data=asdict(guild))

    @staticmethod
    def create_members(members: list[MemberRequestRemote]):
        return post(SawakoAPI.MEMBERS_CREATE_PACK, data=list(map(lambda it: asdict(it), members)))

    @staticmethod
    def fetch_member(member: Member):
        return mapDictToMember(get(SawakoAPI.MEMBERS_FETCH_ONE.format(id=member.id)).json())

    @staticmethod
    def fetch_members():
        return list(map(lambda it: mapDictToMember(it), get(SawakoAPI.MEMBERS_FETCH_ALL).json()))
