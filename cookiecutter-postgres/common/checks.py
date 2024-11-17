from contextlib import suppress

import discord
from discord.ext.commands.core import check
from redbot.core import commands


def ensure_db_connection():
    """Decorator to ensure a database connection is active.

    Example:
    ```python
    @ensure_db_connection()
    @commands.command()
    async def mycommand(self, ctx):
        await ctx.send("Database connection is active")
    ```
    """

    async def predicate(ctx: commands.Context) -> bool:
        if not ctx.cog.db:
            txt = "Database connection is not active, try again later"
            with suppress(discord.HTTPException):
                await ctx.send(txt, ephemeral=True)
            return False
        return True

    return check(predicate)
