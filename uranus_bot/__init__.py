""" Xiaomi Geeks Telegram Bot initialization"""
import logging
from os.path import dirname

import yaml

from uranus_bot.database.database import Database

WORK_DIR = dirname(__file__)
PARENT_DIR = '/'.join(dirname(__file__).split('/')[:-1])

# read bog config
with open(f'{PARENT_DIR}/config.yml', 'r') as f:
    CONFIG = yaml.load(f, Loader=yaml.CLoader)
API_KEY = CONFIG['api_key']
API_HASH = CONFIG['api_hash']
BOT_TOKEN = CONFIG['tg_bot_token']
BOT_ID = CONFIG['tg_bot_id']

# set logging
logging.basicConfig(filename=f'{PARENT_DIR}/tgbot.log',
                    filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# other global variables
HELP_URL = "https://xiaomifirmwareupdater.com/projects/uranus-chatbot/#usage"
XFU_WEBSITE = "http://www.xiaomifirmwareupdater.com"
TG_CHANNEL = "https://t.me/yshalsager_projects"

# set Database
DATABASE = Database(f"{PARENT_DIR}/{CONFIG['tg_bot_db']}")
DATABASE.create_table(f"""CREATE TABLE IF NOT EXISTS chats (
                                    id NUMERIC NOT NULL PRIMARY KEY,
                                    username text UNIQUE, name text, type text); """)
