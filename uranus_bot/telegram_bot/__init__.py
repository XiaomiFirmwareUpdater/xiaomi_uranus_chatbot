""" Telegram bot initialization """
import logging

from uranus_bot.database.database import tg_session, Database

# set logging
TG_LOGGER = logging.getLogger(__name__)
# set Database
DATABASE = Database(tg_session)
