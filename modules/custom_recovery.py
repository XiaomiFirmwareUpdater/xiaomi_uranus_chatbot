#!/usr/bin/env python3.7
"""custom recovery downloads scraper"""

from collections import OrderedDict
import xml.etree.ElementTree as eT
from bs4 import BeautifulSoup
from requests import get
from .mwt import MWT
from .extras import check_codename


@MWT(timeout=60*60*6)
def load_twrp_data():
    """
    load devices info every six hours
    :returns sorted_data
    """
    data = {}
    response = get('https://twrp.me/Devices/Xiaomi/')
    page = BeautifulSoup(response.content, 'html.parser')
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
        data.update({codename: info})
    sorted_data = OrderedDict(sorted(data.items()))
    return sorted_data


@MWT(timeout=60*60*6)
def twrp(device):
    """
    fetch latest twrp links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    status = None
    data = load_twrp_data()
    if device not in list(data.keys()):
        message = f"Can't find downloads for {device}!"
        status = False
        return message, status
    name = data[device]['name']
    link = data[device]['link']
    page = BeautifulSoup(get(link).content, 'html.parser').find('table').find('tr')
    download = page.find('a')
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    message = f'*Latest TWRP for {name}:*\n' \
        f'[{dl_file}]({dl_link}) - {size}\n' \
        f'*Updated:* {date}\n'
    return message, status


@MWT(timeout=60*60*6)
def load_pbrp_data():
    """
    load latest xml files every six hours
    :returns data
    """
    rss = get(
        "https://sourceforge.net/projects/pitchblack-twrp/rss?path=/").text
    data = eT.fromstring(rss)
    return data


@MWT(timeout=60*60*6)
@check_codename
def pbrp(device):
    """
    fetch latest pbrp links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    data = load_pbrp_data()
    links = [i.find('link').text for i in data[0].findall('item')]
    try:
        link = [i for i in links if device in i][0]
    except IndexError:
        message = f"Can't find downloads for {device}!"
        status = False
        return message, status
    file = link.split('/')[-2]
    message = f'[{file}]({link})\n'
    status = True
    return message, status


@MWT(timeout=60*60*2)
def load_ofrp_data():
    """
    load latest json file every six hours
    :returns data
    """
    data = get("https://files.orangefox.tech/Others/update.json").json()
    return data


@MWT(timeout=60*60*2)
@check_codename
def ofrp(device):
    """
    fetch latest ofrp links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    data = load_ofrp_data()
    stable = data['stable']
    beta = data['beta']
    stable_info = {key: value for key, value in stable.items() if device in key}
    beta_info = {key: value for key, value in beta.items() if device in key}
    message = ''
    if not stable_info and not beta_info:
        message = f"Can't find downloads for {device}!"
        status = False
        return message, status
    builds = {}
    if stable_info:
        builds.update({'stable': stable_info})
    if beta_info:
        builds.update({'beta': beta_info})
    for build, data in builds.items():
        name = data[device]['fullname']
        file = data[device]['ver']
        maintainer = data[device]['maintainer']
        notes = data[device]['msg']
        readme = data[device]['readme']
        if build == 'stable':
            branch = 'Stable'
        else:
            branch = 'Beta'
        url = f'https://files.orangefox.tech/OrangeFox-{branch}'
        link = f'{url}/{device}/{file}'
        if not message:
            message += f'Latest {name} (`{device}`) OrangeFox Builds:\n' \
                f'_Maintainer:_ {maintainer}\n'
        message += f'*{branch}:* [{file}]({link})\n'
        if notes:
            message += f'_Notes:_ {notes}\n'
        if readme:
            message += f'README: [Here]({url}/{device}/{readme})\n'
    status = True
    return message, status
