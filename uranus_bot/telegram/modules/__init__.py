""" Xiaomi Geeks Telegram Bot modules loader"""
from os.path import dirname

from uranus_bot import LOGGER
from uranus_bot.utils.loader import get_modules

ALL_MODULES = get_modules(dirname(__file__))
LOGGER.info("Modules to load: %s", str(ALL_MODULES))
# __all__ = ALL_MODULES + ["ALL_MODULES"]
