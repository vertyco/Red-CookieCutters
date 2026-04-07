from redbot.core import commands

from ..abc import MixinMeta


class Admin(MixinMeta):
    @commands.group(name="admingroup")
    @commands.is_owner()
    async def admingroup(self, ctx: commands.Context):
        """"""
