"""twrp custom recovery downloads scraper"""

from bs4 import BeautifulSoup
from aiohttp import ClientSession

from uranus_bot.providers.utils.utils import fetch


async def load_twrp_data():
    """
    load twrp for Xiaomi devices info
    """
    async with ClientSession() as session:
        html = await fetch(session, 'https://twrp.me/Devices/Xiaomi/')
        page = BeautifulSoup(html, 'html.parser')
        devices = page.find("ul", {"class": "post-list"}).findAll('a')
        data = {}
        for i in devices:
            info = {}
            codename = i.text.split('(')[-1].split(')')[0]
            if '/' in codename:
                codename = codename.split('/')[0]
            link = f'https://dl.twrp.me/{codename}/'
            device = i.text
            info.update({'name': device})
            info.update({'link': link})
            data.update({codename: info})
        return data


async def get_twrp(twrp_data, device):
    """
    fetch latest twrp links for a device
    """
    if device not in list(twrp_data.keys()):
        return
    name = twrp_data[device]['name']
    link = twrp_data[device]['link']
    async with ClientSession() as session:
        html = await fetch(session, link)
        page = BeautifulSoup(html, 'html.parser').find('table').find('tr')
        download = page.find('a')
        dl_link = f"https://dl.twrp.me{download['href']}"
        dl_file = download.text
        size = page.find("span", {"class": "filesize"}).text
        date = page.find("em").text.strip()
        return {'name': name, 'dl_file': dl_file, 'dl_link': dl_link, 'size': size, 'date': date}
