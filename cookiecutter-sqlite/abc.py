from abc import ABC, ABCMeta, abstractmethod

from discord.ext.commands.cog import CogMeta
from piccolo.engine.sqlite import SQLiteEngine
from redbot.core.bot import Red


class CompositeMetaClass(CogMeta, ABCMeta):
    """Type detection"""


class MixinMeta(ABC):
    """Type hinting"""

    def __init__(self, *_args):
        self.bot: Red
        self.db: SQLiteEngine | None

    @abstractmethod
    async def initialize(self) -> None:
        raise NotImplementedError
