from disnake.ext import commands


class Client(commands.Bot):
    def __init__(self, **args):
        super().__init__(args)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            # self.add_view()
            self.persistent_views_added = True

        print(f"Logged in as {self.user} (ID: {self.user.id})\n------")
