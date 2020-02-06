#!/usr/bin/env python3.7
"""Xiaomi Firmware Updater commands"""

import yaml
from requests import get
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .mwt import MWT
from .extras import check_codename


@MWT(timeout=60 * 60 * 6)
def fetch_devices():
    """
    fetches devices data every 6h
    :return: devices
    """
    return yaml.load(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/firmware_codenames.yml").text, Loader=yaml.CLoader)


@check_codename(fetch_devices(), markup=True)
def gen_fw_link(device):
    """
    generate latest firmware links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    """
    site = 'https://xiaomifirmwareupdater.com'
    message = f"*Available firmware downloads for* `{device}`\n"
    latest = InlineKeyboardButton(f"Latest Firmware", f"{site}/firmware/{device}/")
    archive = InlineKeyboardButton(f"Firmware Archive", f"{site}/archive/firmware/{device}/")
    channel = InlineKeyboardButton("XiaomiFirmwareUpdater", url="https://t.me/XiaomiFirmwareUpdater")
    reply_markup = InlineKeyboardMarkup([[latest, archive], [channel]])
    return message, reply_markup
