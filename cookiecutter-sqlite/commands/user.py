from redbot.core import commands

from ..abc import MixinMeta
from ..common.checks import ensure_db_connection


class User(MixinMeta):
    @commands.hybrid_command(name="test", description="Some description!")
    @commands.cooldown(1, 15, commands.BucketType.channel)
    @ensure_db_connection()
    async def do_thing(self, ctx: commands.Context):
        """Test command"""
        await ctx.send("TEST")
