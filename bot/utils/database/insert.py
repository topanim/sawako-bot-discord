from disnake import Guild

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Guild import GuildRequestRemote
from bot.api.models.Member import MemberRequestRemote
from bot.api.models.User import UserRequestRemote


def insert_guild(guild: Guild):
    sawako_api.create_guild(GuildRequestRemote(guild.id))

    for user in guild.members:
        if not user.bot:
            sawako_api.create_user(UserRequestRemote(user.id))
            sawako_api.create_member(MemberRequestRemote(guild.id, user.id))