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
        "xiaomifirmwareupdater.github.io/master/data/devices.json").json()
    return devices


def check_codename(func):
    """check if codename is correct"""
    def wrapper(*args, **kwargs):
        codename = args[0].lower()
        devices = fetch_devices()
        status = False
        if [i for i in devices if codename == i['codename'].split('_')[0]]:
            message, status = func(*args, **kwargs)
        else:
            message = "Wrong codename!"
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
    site = 'https://xiaomifirmwareupdater.com/#'
    stable = site + 'stable/#'
    weekly = site + 'weekly/#'
    message = "*Stable Firmware*: [Here]({})\n" \
              "*Weekly Firmware*: [Here]({})\n" \
              "@XiaomiFirmwareUpdater".format(stable + device, weekly + device)
    return message, status


def gen_rom_link(data):
    """
    generate MIUI rom link using filename
    :argument data - json
    :returns reply - telegram message string
    """
    version = data['versions']['miui']
    file = '_'.join(data['filename'].split('_')[2:])
    link = f'http://bigota.d.miui.com/{version}/{file}'
    reply = f"[{version}]({link}) "
    return reply


@MWT(timeout=60*60)
@check_codename
def fetch_fw_data(device):
    """
    fetch MIUI data from site for device
    :argument device - Xiaomi device codename
    :returns reply - telegram message string
    """
    all_data = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/devices/full/" +
        f"{device}.json").json()
    stable = [i for i in all_data if i['branch'] == 'stable']
    weekly = [i for i in all_data if i['branch'] == 'weekly']
    stable.reverse()
    weekly.reverse()
    global_stable = [i for i in stable if i['type'] == 'Global']
    china_stable = [i for i in stable if i['type'] == 'China']
    global_weekly = [i for i in weekly if i['type'] == 'Global']
    china_weekly = [i for i in weekly if i['type'] == 'China']
    reply = '*Available Stable ROMs:*\n'
    if global_stable:
        reply += '_Global:_\n'
        for i in global_stable:
            reply += gen_rom_link(i)
    if china_stable:
        reply += '\n_China:_\n'
        for i in china_stable:
            reply += gen_rom_link(i)
    reply += '\n*Available Weekly ROMs:*\n'
    if global_weekly:
        reply += '_Global:_\n'
        for i in global_weekly:
            reply += gen_rom_link(i)
    if china_weekly:
        reply += '\n_China:_\n'
        for i in china_weekly:
            reply += gen_rom_link(i)
    return reply


@MWT(timeout=60*60*6)
def load_firmware_devices():
    """
    load latest vendor data form json files
    :returns data - a list with merged stable, weekly, current, and EOL data
    """
    data = get('https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +
               'xiaomifirmwareupdater.github.io/master/data/devices.json').json()
    return data


@check_codename
def history(device):
    """
    get all released MIUI rom for device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    devices = load_firmware_devices()
    status = None
    if not [i for i in devices if device == i['codename'].split('_')[0]]:
        message = "Can't find info about codename!"
        return message, status
    message = ''
    data = fetch_fw_data(device)
    message += data
    return message, status
