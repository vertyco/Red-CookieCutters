import asyncpg
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify

from ..abc import MixinMeta
from ..engine import engine
from ..views.postgres_creds import SetConnectionView


class Admin(MixinMeta):
    @commands.group(name="admingroup")
    @commands.is_owner()
    async def admingroup(self, ctx: commands.Context):
        """"""

    @admingroup.command(name="postgres")
    async def admingroup_postgres(self, ctx: commands.Context):
        """Set the Postgres connection info"""
        await SetConnectionView(self, ctx).start()

    @admingroup.command(name="nukedb")
    async def admingroup_nukedb(self, ctx: commands.Context, confirm: bool):
        """Delete the database for this cog and reinitialize it

        THIS CANNOT BE UNDONE!"""
        if not confirm:
            return await ctx.send(
                f"You must confirm this action with `{ctx.clean_prefix}admingroup nukedb True`"
            )
        config = await self.bot.get_shared_api_tokens("postgres")
        if not config:
            return await ctx.send(
                f"Postgres credentials not set! Use `{ctx.clean_prefix}admingroup postgres` command!"
            )

        conn = None
        try:
            try:
                conn = await asyncpg.connect(**config)
            except asyncpg.InvalidPasswordError:
                return await ctx.send("Invalid password!")
            except asyncpg.InvalidCatalogNameError:
                return await ctx.send("Invalid database name!")
            except asyncpg.InvalidAuthorizationSpecificationError:
                return await ctx.send("Invalid user!")

            await conn.execute("DROP DATABASE IF EXISTS cookiecutter-postgres")
        finally:
            if conn:
                await conn.close()

        await self.initialize()
        await ctx.send("Database has been nuked and reinitialized")

    @admingroup.command(name="diagnose")
    async def admingroup_diagnose(self, ctx: commands.Context):
        """Check the database connection"""
        config = await self.bot.get_shared_api_tokens("postgres")
        if not config:
            return await ctx.send(
                f"Postgres credentials not set! Use `{ctx.clean_prefix}admingroup postgres` command!"
            )
        issues = await engine.diagnose_issues(self, config)
        for p in pagify(issues, page_length=1980):
            await ctx.send(box(p, lang="python"))
