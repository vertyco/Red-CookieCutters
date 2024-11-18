import asyncio
import json
import logging
import typing as t
from io import BytesIO

from piccolo.engine.sqlite import SQLiteEngine
from redbot.core import commands
from redbot.core.bot import Red

from .abc import CompositeMetaClass
from .commands import Commands
from .db.tables import TABLES, Player
from .engine import engine
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
    __version__ = "0.0.1b"

    def __init__(self, bot: Red):
        super().__init__()
        self.bot: Red = bot
        self.db: SQLiteEngine = None

    def format_help_for_context(self, ctx: commands.Context):
        helpcmd = super().format_help_for_context(ctx)
        txt = "Version: {}\nAuthor: {}".format(self.__version__, self.__author__)
        return f"{helpcmd}\n\n{txt}"

    async def red_get_data_for_user(self, *, user_id: int) -> t.MutableMapping[str, BytesIO]:
        users = await Player.select(Player.all_columns()).where(Player.author_id == user_id)
        return {"data.json": BytesIO(json.dumps(users).encode())}

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int):
        if not self.db:
            return "Data not deleted, database connection is not active"
        await Player.delete().where(Player.author_id == user_id)
        return f"Data for user ID {user_id} has been deleted"

    async def cog_load(self) -> None:
        asyncio.create_task(self.initialize())

    async def cog_unload(self) -> None:
        pass

    async def initialize(self) -> None:
        await self.bot.wait_until_red_ready()
        log.info("Registering database connection")
        self.db = await engine.register_cog(self, TABLES, trace=True)
        log.info("Database connection established")
