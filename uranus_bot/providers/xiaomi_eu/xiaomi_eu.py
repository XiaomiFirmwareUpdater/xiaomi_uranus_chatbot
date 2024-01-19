"""Xiaomi.eu downloads scraper"""
import json
import re
import xml.etree.ElementTree as eT

from aiohttp import ClientSession

from uranus_bot import GITHUB_ORG
from uranus_bot.providers.utils.utils import fetch


async def load_eu_data():
    """
    load Xiaomi.eu devices downloads
    """
    eu_url = "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/rss?path=/xiaomi.eu"
    async with ClientSession() as session:
        miui_stable = eT.fromstring(await fetch(session, f'{eu_url}/MIUI-STABLE-RELEASES'))
        hyper_os_stable = eT.fromstring(await fetch(session, f'{eu_url}/HyperOS-STABLE-RELEASES'))
        miui_weekly = eT.fromstring(await fetch(session, f'{eu_url}/MIUI-WEEKLY-RELEASES'))
        hyper_os_weekly = eT.fromstring(await fetch(session, f'{eu_url}/HyperOS-WEEKLY-RELEASES'))
        miui_stable_links = [i.find('link').text for i in miui_stable[0].findall('item')]
        hyper_os_stable_links = [i.find('link').text for i in hyper_os_stable[0].findall('item')]
        miui_weekly_links = [i.find('link').text for i in miui_weekly[0].findall('item')]
        hyper_os_weekly_links = [i.find('link').text for i in hyper_os_weekly[0].findall('item')]
        return [*hyper_os_stable_links, *hyper_os_weekly_links, *miui_stable_links, *miui_weekly_links]


async def load_eu_codenames():
    """
    load Xiaomi.eu devices codenames
    """
    async with ClientSession() as session:
        raw = await fetch(session, f'{GITHUB_ORG}/xiaomi_devices/eu/devices.json')
        models = json.loads(raw)
        return models


async def get_eu(codename, eu_data, devices):
    """
    fetch latest xiaomi_eu links for a device
    """
    stable_link = ""
    weekly_link = ""
    device = devices[codename][1]
    try:
        stable_link = [i for i in eu_data if re.search(f"{device}_", i)
                       and re.search(f'{device}_(?:V|OS)', i)][0]
    except IndexError:
        pass
    try:
        weekly_link = [i for i in eu_data if re.search(f"{device}_", i)
                       and re.search(f'{device}_(?:V|OS).*.DEV', i)][0]
    except IndexError:
        pass
    links = [stable_link, weekly_link]
    links_info = {}
    for link in links:
        if not link:
            continue
        links_info.update({link.split('/')[-2].split('_')[-2]: link})
    return links_info
