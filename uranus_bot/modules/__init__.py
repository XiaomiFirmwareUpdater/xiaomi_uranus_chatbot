""" Xiaomi Geeks Telegram Bot modules loader"""
# This code is adapted from
# https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/__init__.py

from glob import glob
from os.path import dirname, isfile

from uranus_bot import LOGGER


def get_modules():
    """Return all modules available in modules directory"""
    return [i.split('/')[-1].split('.')[0] for i in glob(f"{dirname(__file__)}/*.py")
            if i.endswith(".py") and not i.endswith("__init__.py") and isfile(i)]


ALL_MODULES = get_modules()
LOGGER.info("Modules to load: %s", str(ALL_MODULES))
# __all__ = ALL_MODULES + ["ALL_MODULES"]
