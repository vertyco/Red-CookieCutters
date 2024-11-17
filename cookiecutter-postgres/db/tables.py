import logging

from piccolo.columns import BigInt, Serial, Timestamptz
from piccolo.columns.defaults.timestamptz import TimestamptzNow
from piccolo.table import Table, sort_table_classes

log = logging.getLogger("red.cookiecutter")


class User(Table):
    id: Serial
    created_on = Timestamptz()
    modified_on = Timestamptz(auto_update=TimestamptzNow().python)
    user_id = BigInt(help_text="The user ID")


class GuildSettings(Table):
    id: Serial
    created_on = Timestamptz()
    modified_on = Timestamptz(auto_update=TimestamptzNow().python)
    guild_id = BigInt(help_text="The guild ID")


TABLES: list[Table] = sort_table_classes([User, GuildSettings])
