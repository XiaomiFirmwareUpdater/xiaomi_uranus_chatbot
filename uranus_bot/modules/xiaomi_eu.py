#!/usr/bin/env python3.7
"""Xiaomi EU links scraper"""
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, \
    ParseMode
import xml.etree.ElementTree as eT
from requests import get
from .extras import check_codename
from .mwt import MWT


@MWT(timeout=60 * 60 * 6)
def fetch_devices():
    """
    load latest devices data form json file
    :returns data
    """
    data = get('https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +
               'xiaomi_devices/eu/devices.json').json()
    return data


@MWT(timeout=60 * 60)
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


@check_codename(fetch_devices(), markup=True)
def xiaomi_eu(device, inline=False):
    """
    extract latest Xiaomi.eu links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    """
    devices = fetch_devices()
    codename = device
    info = {i: devices[i] for i in devices if i == codename}
    if not info:
        return "", None
    name, device = list(info.values())[0]
    stable, weekly = load_data()
    stable_links = [i.find('link').text for i in stable[0].findall('item')]
    weekly_links = [i.find('link').text for i in weekly[0].findall('item')]
    head = f'*{name}* - `{codename}` latest Xiaomi.eu ROMs:\n'
    message = head
    keyboard = []
    try:
        stable_link = [i for i in stable_links if device == i.split('/')[-2].split('_')[2]][0]
        version = stable_link.split('/')[-2].split('_')[-2]
        stable_markup = InlineKeyboardButton(f"{version}", f"{stable_link}")
        keyboard.append([stable_markup])
    except IndexError:
        pass
    try:
        weekly_link = [i for i in weekly_links if device == i.split('/')[-2].split('_')[2]][0]
        version = weekly_link.split('/')[-2].split('_')[-2]
        weekly_markup = InlineKeyboardButton(f"{version}", f"{weekly_link}")
        keyboard.append([weekly_markup])
    except IndexError:
        pass
    if not keyboard:
        return "", None
    reply_markup = InlineKeyboardMarkup(keyboard)
    if inline:
        results = [InlineQueryResultArticle(
            id=uuid4(),
            title=f"Search {codename} Xiaomi.eu downloads",
            input_message_content=InputTextMessageContent(
                message, parse_mode=ParseMode.MARKDOWN), reply_markup=reply_markup)]
        return results
    else:
        return message, reply_markup
