from redbot.core import commands

from ..abc import MixinMeta


class Admin(MixinMeta):
    @commands.admin_or_permissions(administrator=True)
    async def admincmd(self, ctx: commands.Context):
        """"""
        await ctx.send("beep boop")
