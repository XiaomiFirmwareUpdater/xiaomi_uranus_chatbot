#!/usr/bin/env python3.7
"""Mi Vendor updater"""

import yaml
from requests import get
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .mwt import MWT


@MWT(timeout=60 * 60 * 6)
def fetch_devices():
    """
    fetches devices data every 6h
    :return: devices
    """
    return yaml.load(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/vendor_codenames.yml").text, Loader=yaml.CLoader)


def check_codename(func):
    """check if codename is correct"""
    def wrapper(*args, **kwargs):
        codename = args[0].lower()
        devices = fetch_devices()
        status = False
        reply_markup = None
        if [i for i in devices if codename.split('_')[0] == i]:
            message = func(*args, **kwargs)
            status = True
        else:
            message = f"Can't find vendor downloads for {codename}!"
        return message, status, reply_markup
    return wrapper


@check_codename
def fetch_vendor(device):
    """
    generate latest vendor links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    status = None
    site = 'https://xiaomifirmwareupdater.com'
    message = f"*Available vendor downloads for* `{device}`\n"
    latest = InlineKeyboardButton(f"Latest Vendor", f"{site}/vendor/{device}/")
    archive = InlineKeyboardButton(f"Vendor Archive", f"{site}/archive/vendor/{device}/")
    channel = InlineKeyboardButton("MIUIVendorUpdater", url="https://t.me/MIUIVendorUpdater")
    reply_markup = InlineKeyboardMarkup([[latest, archive], [channel]])
    return message, status, reply_markup
