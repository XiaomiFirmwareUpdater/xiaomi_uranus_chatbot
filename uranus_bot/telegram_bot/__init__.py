""" Telegram bot initialization """
# pylint: disable=wrong-import-position

import logging
from sys import path

path.append("..")

from uranus_bot.database.database import Database
from uranus_bot import PARENT_DIR, TG_BOT_DB

# set logging
TG_LOGGER = logging.getLogger(__name__)
# set Database
DATABASE = Database(f"{PARENT_DIR}/{TG_BOT_DB}")
DATABASE.create_table(f"""CREATE TABLE IF NOT EXISTS chats (
                                    id NUMERIC NOT NULL PRIMARY KEY,
                                    username text UNIQUE, name text, type text); """)
