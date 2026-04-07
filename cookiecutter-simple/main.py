import asyncio
import logging
import typing as t

from redbot.core import Config, commands
from redbot.core.bot import Red

log = logging.getLogger("red.your_cog_name.cookiecutter")
RequestType = t.Literal["discord_deleted_user", "owner", "user", "user_strict"]


class CookieCutter(commands.Cog):
    """Description"""

    __author__ = "[Author Name]"
    __version__ = "0.0.1"

    def __init__(self, bot: Red):
        super().__init__()
        self.bot: Red = bot
        self.config = Config.get_conf(self, 117, force_registration=True)

    def format_help_for_context(self, ctx: commands.Context):
        helpcmd = super().format_help_for_context(ctx)
        txt = "Version: {}\nAuthor: {}".format(self.__version__, self.__author__)
        return f"{helpcmd}\n\n{txt}"

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int):
        return

    async def red_get_data_for_user(self, *, requester: RequestType, user_id: int):
        return

    async def cog_load(self) -> None:
        asyncio.create_task(self.initialize())

    async def cog_unload(self) -> None:
        pass

    async def initialize(self) -> None:
        await self.bot.wait_until_red_ready()
