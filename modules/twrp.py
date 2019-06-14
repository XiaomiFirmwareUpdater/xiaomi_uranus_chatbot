#!/usr/bin/env python3.7
"""TWRP links scraper"""

from collections import OrderedDict
from bs4 import BeautifulSoup
from requests import get
from .mwt import MWT


@MWT(timeout=60*60*6)
def load_data():
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
    data = load_data()
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
