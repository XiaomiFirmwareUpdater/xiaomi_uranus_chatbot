""" Telegram bot initialization """
import logging
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from uranus_bot.database.database import tg_session, Database

# set logging
TG_LOGGER = logging.getLogger(__name__)
# set Database
DATABASE = Database(tg_session)
