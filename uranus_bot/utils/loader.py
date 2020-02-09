""" Xiaomi Geeks chat Bot modules dynamic loader"""
# This code is adapted from
# https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/__init__.py

from glob import glob
from os.path import dirname, isfile


def get_modules(modules_path):
    """Return all modules available in modules directory"""
    return [i.split('/')[-1].split('.')[0] for i in glob(f"{modules_path}/*.py")
            if i.endswith(".py") and not i.endswith("__init__.py") and isfile(i)]
