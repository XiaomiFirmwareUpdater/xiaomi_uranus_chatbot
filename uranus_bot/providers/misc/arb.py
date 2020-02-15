"""ARB info scraper"""

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from uranus_bot.providers.misc import WIKI, XDA
from uranus_bot.providers.utils.utils import fetch


async def get_arb_table():
    """ Get Anti-rollback information photo """
    async with ClientSession() as session:
        page = BeautifulSoup(
            await fetch(session, 'https://xiaomi.eu/community/link-forums/roms-download.73/'),
            'html.parser')
        img = page.findAll('img', {"class": "bbImage"})[1]['src']
        return img


async def get_arb_guides():
    """Anti-Rollback Protection info"""
    return [{
        "About Anti-Rollback Protection": f"{WIKI}/About_Anti-Rollback_Protection.html",
        "Xiaomi’s Anti-Rollback Protection Explained":
            f"{XDA}/xiaomi-anti-rollback-protection-brick-phone/"
    }]
