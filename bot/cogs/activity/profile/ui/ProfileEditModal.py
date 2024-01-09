from disnake import TextInputStyle, ModalInteraction
from disnake.ui import TextInput, Modal

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Member import UpdateMemberBioRequestRemote
from bot.cogs.activity.profile.ui.ProfileEmbed import ProfileEmbed
from bot.ui.embeds.success import SuccessEmbed
from bot.utils.types.strings import none_if_empty


class ProfileEditModal(Modal):
    def __init__(self, user, message):
        components = [
            TextInput(
                label="Имя",
                placeholder="Укажите свое настоящее имя",
                custom_id="name",
                required=False,
                style=TextInputStyle.short,
                min_length=2,
                max_length=10
            ),
            TextInput(
                label="Дата Рождения",
                placeholder="В формате ДД.ММ | 01.01",
                custom_id="birthdate",
                required=False,
                style=TextInputStyle.short,
                min_length=5,
                max_length=5
            ),
            TextInput(
                label="Пол",
                placeholder="Мужской/Женский",
                custom_id="gender",
                required=False,
                style=TextInputStyle.short,
                min_length=7,
                max_length=7
            ),
            TextInput(
                label="Обо мне",
                placeholder="Раскажите о себе",
                custom_id="about",
                required=False,
                style=TextInputStyle.paragraph,
                max_length=150,
            )
        ]
        self.user = user
        self.message = message
        super().__init__(title="Изменить профиль", components=components)

    async def callback(self, inter: ModalInteraction):
        bio = UpdateMemberBioRequestRemote(guild_id=inter.guild.id, user_id=inter.author.id)

        for key, val in inter.text_values.items():
            bio.__setattr__(key, none_if_empty(val))

        dto = sawako_api.update_member_bio(bio=bio)

        embed = ProfileEmbed(
            guild=inter.guild,
            user=inter.author,
            dto=dto)

        await self.message.edit(embed=embed)
        await inter.send(embed=SuccessEmbed('Профиль обновлен'), ephemeral=True)
