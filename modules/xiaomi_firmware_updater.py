#!/usr/bin/env python3.7
"""Xiaomi Firmware Updater commands"""

from requests import get
from .mwt import MWT


@MWT(timeout=60*60*6)
def fetch_devices():
    """
    fetches devices data every 6h
    :return: devices
    """
    devices = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/firmware_codenames.json").json()
    return devices


def check_codename(func):
    """check if codename is correct"""
    def wrapper(*args, **kwargs):
        codename = args[0].lower()
        devices = fetch_devices()
        status = False
        if [i for i in devices if codename.split('_')[0] == i]:
            message = func(*args, **kwargs)
            status = True
        else:
            message = f"Can't find anything about {codename}!"
        return message, status
    return wrapper


@check_codename
def gen_fw_link(device):
    """
    generate latest firmware links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    status = None
    site = 'https://xiaomifirmwareupdater.com'

    message = f"[Latest Firmware]({site}/firmware/{device}/)\n" \
        f"[Firmware Archive]({site}/archive/firmware/{device}/)\n" \
        "@XiaomiFirmwareUpdater"
    return message, status


@check_codename
def history(device):
    """
    generate latest firmware links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    status = None
    site = 'https://xiaomifirmwareupdater.com'
    message = f"[MIUI ROMs archive]({site}/archive/miui/{device}/)\n" \
        "@MIUIUpdatesTracker"
    return message, status

