""" Xiaomi Geeks Telegram Bot initialization"""
import logging
import sys
from os.path import dirname

import yaml
import sentry_sdk

from uranus_bot.database.database import Database
from uranus_bot.utils.sentry_logging import sentry_before_send

WORK_DIR = dirname(__file__)
PARENT_DIR = '/'.join(dirname(__file__).split('/')[:-1])

# read bog config
with open(f'{PARENT_DIR}/config.yml', 'r') as f:
    CONFIG = yaml.load(f, Loader=yaml.CLoader)
API_KEY = CONFIG['api_key']
API_HASH = CONFIG['api_hash']
BOT_TOKEN = CONFIG['tg_bot_token']
BOT_ID = CONFIG['tg_bot_id']
TG_BOT_DB = CONFIG['tg_bot_db']
DISCORD_TOKEN = CONFIG['discord_bot_token']
DISCORD_DB = CONFIG['discord_bot_db']
# set logging
# logging.basicConfig(filename=f'{PARENT_DIR}/bot.log',
#                     filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s'
                              '[%(module)s.%(funcName)s:%(lineno)d]: %(message)s')
OUT = logging.StreamHandler(sys.stdout)
ERR = logging.StreamHandler(sys.stderr)
OUT.setFormatter(FORMATTER)
ERR.setFormatter(FORMATTER)
OUT.setLevel(logging.INFO)
ERR.setLevel(logging.WARNING)
LOGGER = logging.getLogger()
LOGGER.addHandler(OUT)
LOGGER.addHandler(ERR)
LOGGER.setLevel(logging.INFO)

# other global variables
HELP_URL = "https://xiaomifirmwareupdater.com/projects/uranus-chatbot/#usage"
XFU_WEBSITE = "http://www.xiaomifirmwareupdater.com"
TG_CHANNEL = "https://t.me/yshalsager_projects"

# Init sentry sdk for errors reporting
# SENTRY_KEY = CONFIG['sentry_sdk_key']
# sentry_sdk.init(SENTRY_KEY, before_send=sentry_before_send)
