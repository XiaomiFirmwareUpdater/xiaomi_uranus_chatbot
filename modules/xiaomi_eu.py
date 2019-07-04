#!/usr/bin/env python3.7
"""Xiaomi EU links scraper"""

import xml.etree.ElementTree as eT
from requests import get
from .extras import check_codename
from .mwt import MWT


@MWT(timeout=60*60*6)
def fetch_devices():
    """
    load latest devices data form json file
    :returns data
    """
    data = get('https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +
               'xiaomi_devices/eu/devices.json').json()
    return data


@MWT(timeout=60*60)
def load_data():
    """
    load latest xml files every one hour
    :returns data
    """
    stable_rss = get(
        "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/rss" +
        "?path=/xiaomi.eu/MIUI-STABLE-RELEASES").text
    stable = eT.fromstring(stable_rss)
    weekly_rss = get(
        "https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/rss" +
        "?path=/xiaomi.eu/MIUI-WEEKLY-RELEASES").text
    weekly = eT.fromstring(weekly_rss)
    return stable, weekly


@check_codename
def xiaomi_eu(device):
    """
    extract latest Xiaomi.eu links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    status = None
    devices = fetch_devices()
    codename = device
    info = {i: devices[i] for i in devices if i == codename}
    if not info:
        message = f"Can't find info about {codename}!"
        status = False
        return message, status
    name, device = list(info.values())[0]
    stable, weekly = load_data()
    stable_links = [i.find('link').text for i in stable[0].findall('item')]
    weekly_links = [i.find('link').text for i in weekly[0].findall('item')]
    head = f'*{name}* - `{codename}` latest Xiaomi.eu ROMs:\n'
    message = head
    try:
        stable_link = [i for i in stable_links if device == i.split('/')[-2].split('_')[2]][0]
        version = stable_link.split('/')[-2].split('_')[-2]
        message += f'[{version}]({stable_link})\n'
    except IndexError:
        pass
    try:
        weekly_link = [i for i in weekly_links if device == i.split('/')[-2].split('_')[2]][0]
        version = weekly_link.split('/')[-2].split('_')[-2]
        message += f'[{version}]({weekly_link})\n'
    except IndexError:
        pass
    if message == head:
        message = f"Can't find info about {codename}!"
        status = False
        return message, status
    return message, status


