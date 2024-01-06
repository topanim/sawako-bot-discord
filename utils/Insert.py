from disnake import Guild

from api.SawakoAPI import sawako_api
from api.models.Guild import GuildRequestRemote
from api.models.Member import MemberRequestRemote
from api.models.User import UserRequestRemote


def insert_guild(guild: Guild):
    sawako_api.create_guild(GuildRequestRemote(guild.id))

    for user in guild.members:
        if not user.bot:
            sawako_api.create_user(UserRequestRemote(user.id))
            sawako_api.create_member(MemberRequestRemote(guild.id, user.id))