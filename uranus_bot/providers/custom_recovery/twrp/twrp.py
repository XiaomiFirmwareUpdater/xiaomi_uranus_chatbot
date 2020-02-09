"""custom recovery downloads scraper"""
import asyncio

from bs4 import BeautifulSoup
from aiohttp import ClientSession

from uranus_bot import LOGGER
from uranus_bot.providers.utils.utils import fetch

TWRP_DATA = {}


async def twrp_data_loop():
    """
    loop devices' info every six hours
    """
    while True:
        LOGGER.info("Refetching twrp data")
        TWRP_DATA.clear()
        await load_twrp_data()
        await asyncio.sleep(60 * 60 * 6)


async def load_twrp_data():
    """
    load twrp for Xiaomi devices info
    """
    async with ClientSession() as session:
        html = await fetch(session, 'https://twrp.me/Devices/Xiaomi/')
        page = BeautifulSoup(html, 'html.parser')
        devices = page.find("ul", {"class": "post-list"}).findAll('a')
        for i in devices:
            info = {}
            codename = i.text.split('(')[-1].split(')')[0]
            if '/' in codename:
                codename = codename.split('/')[0]
            link = f'https://dl.twrp.me/{codename}/'
            device = i.text
            info.update({'name': device})
            info.update({'link': link})
            TWRP_DATA.update({codename: info})


async def get_twrp(device):
    """
    fetch latest twrp links for a device
    :argument device - Xiaomi device codename
    """
    if not TWRP_DATA:
        await load_twrp_data()
    if device not in list(TWRP_DATA.keys()):
        return
    name = TWRP_DATA[device]['name']
    link = TWRP_DATA[device]['link']
    async with ClientSession() as session:
        html = await fetch(session, link)
        page = BeautifulSoup(html, 'html.parser').find('table').find('tr')
        download = page.find('a')
        dl_link = f"https://dl.twrp.me{download['href']}"
        dl_file = download.text
        size = page.find("span", {"class": "filesize"}).text
        date = page.find("em").text.strip()
        return {'name': name, 'dl_file': dl_file, 'dl_link': dl_link, 'size': size, 'date': date}
