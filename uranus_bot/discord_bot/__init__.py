""" Discord bot initialization """
import logging
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from uranus_bot.database.discord_database import Database, discord_session

DISCORD_LOGGER = logging.getLogger(__name__)
# set Database
DATABASE = Database(discord_session)
