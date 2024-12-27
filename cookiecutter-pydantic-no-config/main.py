import asyncio
import logging
import typing as t

from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.data_manager import cog_data_path

from .abc import CompositeMetaClass
from .commands import Commands
from .common.models import DB
from .listeners import Listeners
from .tasks import TaskLoops

log = logging.getLogger("red.cookiecutter")
RequestType = t.Literal["discord_deleted_user", "owner", "user", "user_strict"]


class CookieCutter(
    Commands,
    Listeners,
    TaskLoops,
    commands.Cog,
    metaclass=CompositeMetaClass,
):
    """Description"""

    __author__ = "author name"
    __version__ = "0.0.1"

    def __init__(self, bot: Red):
        super().__init__()
        self.bot: Red = bot
        self.db: DB = DB()
        self.saving = False

    def format_help_for_context(self, ctx: commands.Context):
        helpcmd = super().format_help_for_context(ctx)
        txt = "Version: {}\nAuthor: {}".format(self.__version__, self.__author__)
        return f"{helpcmd}\n\n{txt}"

    async def red_delete_data_for_user(self, *args, **kwargs):
        return

    async def red_get_data_for_user(self, *args, **kwargs):
        return

    async def cog_load(self) -> None:
        asyncio.create_task(self.initialize())

    async def initialize(self) -> None:
        await self.bot.wait_until_red_ready()
        self.db = await asyncio.to_thread(DB.from_file, cog_data_path(self))
        log.info("Config loaded")

    def save(self) -> None:
        async def _save():
            if self.saving:
                return
            try:
                self.saving = True
                await asyncio.to_thread(self.db.to_file, cog_data_path(self))
            except Exception as e:
                log.exception("Failed to save config", exc_info=e)
            finally:
                self.saving = False

        asyncio.create_task(_save())
