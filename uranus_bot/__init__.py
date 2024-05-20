""" Xiaomi Geeks Telegram Bot initialization"""
import logging
import sys
from os.path import dirname

import yaml
from sentry_sdk import init
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.tornado import TornadoIntegration

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
TG_BOT_ADMINS = CONFIG['tg_bot_admins']
TG_BOT_DB = CONFIG['tg_bot_db']
WITH_EXTRA = CONFIG['tg_bot_extra']
DISCORD_TOKEN = CONFIG['discord_bot_token']
DISCORD_DB = CONFIG['discord_bot_db']
DISCORD_BOT_ADMINS = CONFIG['discord_bot_admins']
DEBUG = CONFIG['debug']
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
HELP_URL = "https://xmfirmwareupdater.com/projects/uranus-chatbot/#usage"
XFU_WEBSITE = "https://www.xmfirmwareupdater.com"
TG_CHANNEL = "https://t.me/yshalsager_projects"

# Init sentry sdk for errors reporting
SENTRY_KEY = CONFIG['sentry_sdk_key']
if not DEBUG:
    init(SENTRY_KEY,
         integrations=[AioHttpIntegration(), SqlalchemyIntegration(), TornadoIntegration()],
         before_send=sentry_before_send)
GITHUB_ORG = "https://raw.githubusercontent.com/XiaomiFirmwareUpdater"
