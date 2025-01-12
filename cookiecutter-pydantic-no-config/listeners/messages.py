import discord
from redbot.core import commands

from ..abc import MixinMeta


class MessageListeners(MixinMeta):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass
