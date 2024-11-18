# Advanced SQLite Cookiecutter

This cog template is a more advanced version of the simple cog template. It includes a more robust structure for larger cogs, and utilizes Postgres to store data to enable better scalability and data management.

## Key Components

- Subclassed commands, listeners, and tasks
- SQLite database functionality
- Full ORM via Piccolo
- Automaticly runs migrations on load
- Bundled `build.py` script for easily creating new migrations
- @ensure_db_connection command decorator for ensuring a connection to the database
