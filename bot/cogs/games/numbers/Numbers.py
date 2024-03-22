import asyncio

from disnake import Member, Message, ButtonStyle, Button, MessageInteraction, Embed
from disnake.ext.commands import Cog, Bot, slash_command, Param
from disnake.ui import button, View

from bot.api.SawakoAPI import sawako_api
from bot.api.models.Member import UpdateMemberWalletRequestRemote, MemberRequestRemote
from bot.cogs.games.numbers.ui.GameIsInterrupted import GameIsInterrupted
from bot.cogs.games.numbers.ui.GameRequest import GameRequest
from bot.cogs.games.numbers.ui.Preparation import Preparation
from bot.cogs.games.numbers.ui.WaitingTimeExceeded import WaitingTimeExceededEmbed
from bot.ui.embeds.ErrorEmbed import ErrorEmbed
from bot.utils.cogs.BaseCog import BaseCog
from bot.utils.logging.Logger import Logger

logger = Logger(__file__)


class Numbers(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(logger)
        self.bot = bot

    @slash_command()
    async def numbers(self, inter):
        pass

    @numbers.sub_command(description='Игра в числа')  # Игра в числа
    async def play(
            self,
            inter,
            player2: Member = Param(name="соперник", description="Ваш соперник"),
            author_num: str = Param(name="число",
                                    description="Ваше число, которое должен будет отгадать противник",
                                    min_length=4, max_length=4),
            bet: int = Param(name="ставка", description="Ставка на игру (серверная валюта)",
                             choices=[100, 500, 1000, 5000, 10000], default=0),
            with_zero: str = Param(name="тип", description="Игра с нулем или без",
                                   choices=["С нулем", "Без нуля"], default="Без нуля")
    ):
        if player2.bot:
            embed = ErrorEmbed('Вы не можете играть против бота') \
                .set_footer(text="Перед началом игры, ознакомьтесь с ее правилами /numbers rules",
                            icon_url=inter.guild.icon.url)
            return await inter.response.send_message(embed=embed, ephemeral=True)

        if inter.author == player2:
            embed = ErrorEmbed('Вы не можете играть против себя') \
                .set_footer(text="Перед началом игры, ознакомьтесь с ее правилами /numbers rules",
                            icon_url=inter.guild.icon.url)
            return await inter.response.send_message(embed=embed, ephemeral=True)

        bal1 = sawako_api.fetch_member(MemberRequestRemote(guild_id=inter.guild.id, user_id=inter.author.id)).wallet
        bal2 = sawako_api.fetch_member(MemberRequestRemote(guild_id=inter.guild.id, user_id=inter.author.id)).wallet
        if bal1 < bet or bal2 < bet:
            embed = ErrorEmbed('У одного из игроков недостаточно денег для игры') \
                .set_footer(text="Перед началом игры, ознакомьтесь с ее правилами /numbers rules",
                            icon_url=inter.guild.icon.url)
            return await inter.response.send_message(embed=embed, ephemeral=True)

        if not author_num.isdigit():
            embed = ErrorEmbed('Вводимое значение должно быть числом') \
                .set_footer(text="Перед началом игры, ознакомьтесь с ее правилами /numbers rules",
                            icon_url=inter.guild.icon.url)
            return await inter.response.send_message(embed=embed, ephemeral=True)

        if "0" in author_num and not with_zero:
            embed = ErrorEmbed('Данная игра ведется без нуля, вы не можете его использовать') \
                .set_footer(text="Перед началом игры, ознакомьтесь с ее правилами /numbers rules",
                            icon_url=inter.guild.icon.url)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        if len(set(str(author_num))) != 4:
            embed = ErrorEmbed('Цифры в числе не должны повторяться') \
                .set_footer(text="Перед началом игры, ознакомьтесь с ее правилами /numbers rules",
                            icon_url=inter.guild.icon.url)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        embed = GameRequest(inter.author, bet, with_zero, inter.guild.icon.url)
        await inter.response.send_message(player2.mention, embed=embed)
        message = await inter.original_message()
        await message.edit(
            view=NumGame(
                bot=self.bot,
                message=message,
                author=inter.author,
                author_num=author_num,
                player2=player2,
                bet=bet,
                with_zero=with_zero == "С нулем"))


class NumGame(View):
    def __init__(self, *, bot: Bot, message: Message, author: Member, author_num: str, player2: Member,
                 bet: int, with_zero: bool):
        super().__init__(timeout=1200.0)
        self.bot = bot
        self.message = message
        self.finished = False
        self.with_zero = with_zero
        self.player = player2
        self.bet = bet
        self.hidden_numbers = {author: author_num, player2: None}
        self.reverse = {author: player2, player2: author}
        self.game_progress = "0123456789\n".rjust(33) if with_zero else "123456789\n".rjust(33) + "{}|{}\n".format(
            player2.display_name[:16].center(16), author.display_name[:16].center(16))

    @button(label="Принять", style=ButtonStyle.green, custom_id="confirm")
    async def confirm(self, button: Button, inter: MessageInteraction):
        if inter.author != self.player:
            embed = ErrorEmbed('Вызов отправлен не вам')
            await inter.send(embed=embed, ephemeral=True)
            return

        embed = Preparation(self.player.display_name, inter.guild.icon.url)
        await self.message.edit(content=None, embed=embed, view=None)

        try:
            player2_num = await self.bot.wait_for('message', check=self.validator, timeout=120.0)
            player2_num = self.process_message(player2_num.content)
        except TimeoutError:
            embed = WaitingTimeExceededEmbed(self.player.display_name)
            return await self.message.edit(embed=embed)

        if player2_num == "0000":
            self.finish_game(inter.guild)
            self.finished = True

            embed = Embed(title="Игра была прервана", description=f"{self.player} прервал игру")
            return await self.message.edit(embed=embed)

        self.hidden_numbers[self.player] = player2_num

        for member in self.hidden_numbers:
            embed = Embed(title="Числа", description=f"Загаданное вами число - {self.hidden_numbers[member]}")
            await member.send(embed=embed)

        embed = Embed(title="Числа", description=f"```py\n{self.game_progress}```")
        while True:
            for self.player in self.hidden_numbers:
                embed.set_footer(text=f"ходит - {self.player}", icon_url=self.player.display_avatar.url)
                await self.message.edit(embed=embed)

                try:
                    move = await self.bot.wait_for('message', check=self.validator, timeout=180.0)
                except asyncio.TimeoutError:
                    embed = WaitingTimeExceededEmbed(self.player.display_name)
                    return await self.message.edit(embed=embed)
                await move.delete()

                if move.content == "0000":
                    self.finish_game(inter.guild)
                    self.finished = True

                    embed = GameIsInterrupted(self.player.display_name)
                    return await self.message.edit(embed=embed)

                result = self.move_result(move.content, self.hidden_numbers[self.reverse[self.player]])
                self.game_progress += result

                embed = Embed(title="Числа", description=f"```py\n{self.game_progress}```")
                if result.replace(" ", "")[-3:] != "4:4":
                    await self.message.edit(embed=embed)
                else:
                    self.finish_game(inter.guild)
                    self.finished = True

                    embed.set_footer(text=f"Победитель - {self.player.display_name} | {self.bet}$".center(33),
                                     icon_url=self.player.display_avatar.url)
                    return await self.message.edit(embed=embed)
            self.game_progress += "\n"

    @button(label="Отказаться", style=ButtonStyle.red, custom_id="not_confirm")
    async def not_confirm(self, button: Button, inter: MessageInteraction):
        if inter.author != self.player:
            embed = ErrorEmbed('Вызов отправлен не вам')
            await inter.send(content=None, embed=embed, ephemeral=True)

        embed = Embed(title="Увы", description=f"{self.player.mention} отказался")
        await self.message.edit(embed=embed, view=None)

    async def on_timeout(self):
        if not self.finished:
            embed = Embed(title="Время вышло", description="Время отведенное на игру вышло")
            await self.message.edit(embed=embed)

    @staticmethod
    def process_message(message: str) -> str:
        return message.replace("|", "")

    def validator(self, mess: Message) -> bool:
        processed_message = self.process_message(mess.content)

        if mess.author != self.player:
            return False

        if processed_message == "0000":
            return True

        if not processed_message.isdigit():
            return False

        if len(processed_message) != 4:
            return False

        if "0" in processed_message and not self.with_zero:
            return False

        if len(set(processed_message)) != 4:
            return False

        return True

    @classmethod
    def how_many_in(cls, move: str, num: str):
        count = 0
        for char in move:
            if char in num:
                count += 1

        return count

    @classmethod
    def how_many_in_their_places(cls, move: str, num: str):
        count = 0
        for i in range(4):
            if move[i] == num[i]:
                count += 1

        return count

    @classmethod
    def move_result(cls, move: str, num: str):
        return "{}-{}:{}".format(
            move,
            cls.how_many_in(move, num),
            cls.how_many_in_their_places(move, num)).center(16)

    def finish_game(self, guild):
        sawako_api.update_member_wallet(
            UpdateMemberWalletRequestRemote(
                guild_id=guild.id,
                user_id=self.reverse[self.player].id,
                amount=self.bet))

        sawako_api.update_member_wallet(
            UpdateMemberWalletRequestRemote(
                guild_id=guild.id,
                user_id=self.player.id,
                amount=-self.bet))
