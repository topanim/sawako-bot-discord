from dataclasses import asdict

from requests import get, post

from bot.api.cache.guilds import guilds_cache
from bot.api.models.Guild import GuildRequestRemote, mapDictToGuild, GuildDTO
from bot.api.models.Member import MemberRequestRemote, mapDictToMember, MemberDTO, UpdateMemberBioRequestRemote, \
    UpdateMemberWalletRequestRemote, UpdateMemberExpRequestRemote, mapDictToUpdatedMember
from bot.api.models.User import UserRequestRemote, mapDictToUser, UserDTO
from bot.utils.logging.Logger import Logger
from bot.utils.logging.decorators.on_error import on_error

logger = Logger(__file__)


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
    MEMBERS_FETCH_ONE = BASE_URL + "members/one/"
    MEMBERS_MARRY = BASE_URL + "members/marry"
    MEMBERS_DIVORCE = BASE_URL + "members/divorce"
    MEMBERS_UPDATE_BIO = BASE_URL + "members/update/bio"
    MEMBERS_UPDATE_EXP_ADD = BASE_URL + "members/update/exp"
    MEMBERS_UPDATE_WALLET = BASE_URL + "members/update/wallet"
    MEMBERS_RESET_BIO = BASE_URL + "members/bio/reset"
    MEMBERS_DELETE = BASE_URL + "members/delete"

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def create_user(user: UserRequestRemote):
        return post(SawakoAPI.USERS_CREATE, json=asdict(user))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def fetch_user(user_id: int):
        return mapDictToUser(get(SawakoAPI.USERS_FETCH_ONE.format(id=user_id)).json())

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def fetch_users():
        return list(map(lambda it: mapDictToUser(it), get(SawakoAPI.USERS_FETCH_ALL).json()))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def delete_user(user: UserDTO):
        return post(SawakoAPI.USERS_DELETE.format(id=user.id))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def create_guild(guild: GuildRequestRemote):
        return post(SawakoAPI.GUILDS_CREATE, json=asdict(guild))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def fetch_guild(guild_id: int):
        return mapDictToGuild(get(SawakoAPI.GUILDS_FETCH_ONE.format(id=guild_id)).json())

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def fetch_guilds():
        return list(map(lambda it: mapDictToGuild(it), get(SawakoAPI.GUILDS_FETCH_ALL).json()))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def delete_guild(guild: GuildDTO):
        return post(SawakoAPI.USERS_DELETE.format(id=guild.id))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def create_member(member: MemberRequestRemote):
        return post(SawakoAPI.MEMBERS_CREATE, json=asdict(member))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def fetch_member(member: MemberRequestRemote):
        return mapDictToMember(get(
            SawakoAPI.MEMBERS_FETCH_ONE, json=asdict(member)).json())

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def fetch_members():
        return list(map(lambda it: mapDictToMember(it), get(SawakoAPI.MEMBERS_FETCH_ALL).json()))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def fetch_members_top(guild):
        return list(map(lambda it: mapDictToMember(it),
                        get(SawakoAPI.MEMBERS_FETCH_TOP.format(id=guild)).json()))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def fetch_members_from_guild(guild: int):
        return list(map(lambda it: mapDictToMember(it),
                        get(SawakoAPI.MEMBERS_FETCH_ALL_FROM_GUILD.format(id=guild)).json()))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def update_member_bio(bio: UpdateMemberBioRequestRemote):
        return mapDictToMember(post(SawakoAPI.MEMBERS_UPDATE_BIO, json=asdict(bio)).json())

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def update_member_exp_add(request_remote: UpdateMemberExpRequestRemote):
        return mapDictToUpdatedMember(post(SawakoAPI.MEMBERS_UPDATE_EXP_ADD, json=asdict(request_remote)).json())

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def update_member_wallet(request_remote: UpdateMemberWalletRequestRemote):
        return post(SawakoAPI.MEMBERS_UPDATE_WALLET, json=asdict(request_remote))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def divorce_members(request_remote: MemberRequestRemote):
        return post(SawakoAPI.MEMBERS_RESET_BIO, json=asdict(request_remote))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def marry_members(request_remotes: list[MemberRequestRemote]):
        return post(
            SawakoAPI.MEMBERS_MARRY,
            json=[asdict(request_remotes[0]), asdict(request_remotes[1])])

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def reset_member_bio(request_remote: MemberRequestRemote):
        return mapDictToMember(post(SawakoAPI.MEMBERS_RESET_BIO, json=asdict(request_remote)).json())

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def delete_member(request_remote: MemberRequestRemote):
        return post(SawakoAPI.MEMBERS_DELETE, json=asdict(request_remote))

    @staticmethod
    @on_error(logger, Logger.ERROR)
    def update_guilds_cache():
        guilds = sawako_api.fetch_guilds()
        guilds_cache.clear()

        for guild in guilds:
            guilds_cache[guild.id] = guild.settings


sawako_api = SawakoAPI()
