""" Discord bot initialization """
# pylint: disable=wrong-import-position

import logging
from sys import path

path.append("..")

from uranus_bot.database.database import Database
from uranus_bot import PARENT_DIR, DISCORD_DB

DISCORD_LOGGER = logging.getLogger(__name__)

# set Database
DATABASE = Database(f"{PARENT_DIR}/{DISCORD_DB}")
DATABASE.create_table(f"""CREATE TABLE IF NOT EXISTS chats (
                                    id NUMERIC NOT NULL PRIMARY KEY,
                                    username text UNIQUE, name text, type text); """)
