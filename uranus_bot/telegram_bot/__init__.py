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
DATABASE.create_table(f"""CREATE TABLE IF NOT EXISTS subscriptions (
                                    id NUMERIC NOT NULL, chat_type text,
                                    sub_type text, device text); """)
DATABASE.create_table(f"""CREATE TABLE IF NOT EXISTS i18n (
                                    id NUMERIC NOT NULL PRIMARY KEY, lang text); """)
DATABASE.create_table(f"""CREATE TABLE IF NOT EXISTS devices (
                                    id NUMERIC NOT NULL PRIMARY KEY, device text); """)
