from disnake import Button, MessageInteraction
from disnake.ui import View, button

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Member import MemberRequestRemote
from bot.cogs.activity.profile.ui.ProfileEditModal import ProfileEditModal
from bot.cogs.activity.profile.ui.ProfileEmbed import ProfileEmbed
from bot.ui.embeds.ErrorEmbed import ErrorEmbed
from bot.ui.embeds.SuccessEmbed import SuccessEmbed


class ProfileEditButtons(View):
    def __init__(self, author, message):
        self.author = author
        self.message = message
        super().__init__(timeout=60.0)

    @button(label='Изменить')
    async def setprofile(self, button: Button, inter: MessageInteraction):
        if inter.author != self.author:
            embed = ErrorEmbed('Вам не доступно это взаимодействие')
            return await inter.send(embed=embed, ephemeral=True)

        await inter.response.send_modal(modal=ProfileEditModal(self.author, self.message))

    @button(label='Сбросить')
    async def clear_profile(self, button: Button, inter: MessageInteraction):
        if inter.author != self.author:
            embed = ErrorEmbed('Вам не доступно это взаимодействие')
            return await inter.send(embed=embed, ephemeral=True)

        dto = sawako_api.reset_member_bio(MemberRequestRemote(inter.guild.id, self.author.id))

        embed = ProfileEmbed(
            guild=inter.guild,
            user=inter.author,
            dto=dto)

        await self.message.edit(embed=embed)
        await inter.send(embed=SuccessEmbed('Профиль успешно сброшен'))

    async def on_timeout(self):
        await self.message.edit(view=None)
