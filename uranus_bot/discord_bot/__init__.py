""" Discord bot initialization """
import logging

from uranus_bot.database.discord_database import Database, discord_session

DISCORD_LOGGER = logging.getLogger(__name__)
# set Database
DATABASE = Database(discord_session)
