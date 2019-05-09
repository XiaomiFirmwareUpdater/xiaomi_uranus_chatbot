#!/usr/bin/env python3.7
"""Xiaomi Helper Bot general commands"""

import json
import re
from requests import get

codenames = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/xiaomi_devices/" +
        "master/devices.json").content)


def check_codename(codename):
    """check if codename is correct"""
    if not [i for i in codenames['data'] if codename == i.split('_')[0]]:
        return False
    else:
        return True


def load_fastboot_data(device):
    """
    load latest fasboot ROMs data form MIUI tracker json files
    :argument device - Xiaomi device codename
    :returns data - a list with merged stable, weekly, current, and EOL data
    """
    stable_roms = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "stable_fastboot/stable_fastboot.json").content)
    weekly_roms = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "weekly_fastboot/weekly_fastboot.json").content)
    eol_stable_roms = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "stable_fastboot/stable_fastboot.json").content)
    eol_weekly_roms = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "weekly_fastboot/weekly_fastboot.json").content)
    latest_stable = [i for i in stable_roms
                     if device == i['codename'].split('_')[0] and i['version']]
    latest_weekly = [i for i in weekly_roms
                     if device == i['codename'].split('_')[0] and i['version']]
    eol_stable = [i for i in eol_stable_roms
                  if device == i['codename'].split('_')[0] and i['version']]
    eol_weekly = [i for i in eol_weekly_roms
                  if device == i['codename'].split('_')[0] and i['version']]
    data = latest_stable + latest_weekly + eol_stable + eol_weekly
    return data


def fetch_recovery(device):
    """
    fetch latest recovery ROMs for a device from MIUI updates tracker json files
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    stable_roms = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "stable_recovery/stable_recovery.json").content)
    weekly_roms = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "weekly_recovery/weekly_recovery.json").content)
    eol_stable_roms = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "stable_recovery/stable_recovery.json").content)
    eol_weekly_roms = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "weekly_recovery/weekly_recovery.json").content)
    latest_stable = [i for i in stable_roms
                     if device == i['codename'].split('_')[0] and i['version']]
    latest_weekly = [i for i in weekly_roms
                     if device == i['codename'].split('_')[0] and i['version']]
    eol_stable = [i for i in eol_stable_roms
                  if device == i['codename'].split('_')[0] and i['version']]
    eol_weekly = [i for i in eol_weekly_roms
                  if device == i['codename'].split('_')[0] and i['version']]
    data = latest_stable + latest_weekly + eol_stable + eol_weekly
    message = ''
    status = None
    if not data:
        message = "No such device!"
        status = False
        return message, status
    for i in data:
        name = i['device']
        version = i['version']
        android = i['android']
        download = i['download']
        if 'V' in version:
            rom_type = 'Stable'
        else:
            rom_type = 'Weekly'
        message += "Latest {} {} ROM:\n" \
                   "*Version:* `{}` \n" \
                   "*Android:* {} \n" \
                   "*Download*: [Here]({}) \n\n" \
            .format(name, rom_type, version, android, download)
    return message, status


def fetch_fastboot(device):
    """
    fetch latest fastboot ROMs for a device from MIUI updates tracker json files
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    status = None
    data = load_fastboot_data(device)
    if not data:
        message = "No such device!"
        status = False
        return message, status
    for i in data:
        name = i['device']
        version = i['version']
        android = i['android']
        download = i['download']
        if 'V' in version:
            rom_type = 'Stable'
        else:
            rom_type = 'Weekly'
        message += "Latest {} {} ROM:\n" \
                   "*Version:* `{}` \n" \
                   "*Android:* {} \n".format(name, rom_type, version, android)
        message += "*Download*: [Here]({}) \n\n".format(download)
    return message, status


def gen_fw_link(device):
    """
    generate latest firmware links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    devices = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/devices.json").content)
    status = None
    if not [i for i in devices if device == i['codename'].split('_')[0]]:
        message = "Wrong codename!"
        status = False
        return message, status
    site = 'https://xiaomifirmwareupdater.com/#'
    stable = site + 'stable/#'
    weekly = site + 'weekly/#'
    message = "*Stable Firmware*: [Here]({})\n" \
              "*Weekly Firmware*: [Here]({})\n".format(stable + device, weekly + device)
    return message, status


def check_latest(device):
    """
    check latest version of ROMs for a device from MIUI updates tracker json files
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    status = None
    data = load_fastboot_data(device)
    if not data:
        message = "No such device!"
        status = False
        return message, status
    for i in data:
        version = i['version']
        if 'V' in version:
            branch = 'Stable'
        else:
            branch = 'Weekly'
        file = i['filename']
        if 'eea_global' in file:
            region = 'EEA Global'
        elif 'in_global' in file:
            region = 'India'
        elif 'ru_global' in file:
            region = 'Russia'
        elif 'global' in file:
            region = 'Global'
        else:
            region = 'China'
        message += "Latest {} {}: `{}`\n".format(region, branch, version)
    return message, status


def oss(device):
    """
    get latest oss kernel for a device from MIUI Mi Code repo
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    info = list(get(
        "https://raw.githubusercontent.com/MiCode/Xiaomi_Kernel_OpenSource/" +
        "README/README.md").text.splitlines())
    data = [i.split('|')[-2] for i in info if device in i]
    message = ''
    status = None
    if not data:
        message = "No such device!"
        status = False
        return message, status
    for item in data:
        message += "{}\n".format(item.strip())
    return message, status


def history(device):
    """
    get all released MIUI rom for device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    devices = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/devices.json").content)
    status = None
    if not [i for i in devices if device == i['codename'].split('_')[0]]:
        message = "Wrong codename!"
        return message, status
    all_data = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/devices/full/" +
        "{}.json".format(device)).content)
    stable = [i for i in all_data if i['branch'] == 'stable']
    weekly = [i for i in all_data if i['branch'] == 'weekly']
    stable.reverse()
    weekly.reverse()
    message = '*Available Stable ROMs:*\n'
    for i in stable:
        version = i['versions']['miui']
        file = '_'.join(i['filename'].split('_')[2:])
        link = 'http://bigota.d.miui.com/{}/{}'.format(version, file)
        message += "[{}]({}) ".format(version, link)
    message += '\n*Available Weekly ROMs:*\n'
    for i in weekly:
        version = i['versions']['miui']
        file = '_'.join(i['filename'].split('_')[2:])
        link = 'http://bigota.d.miui.com/{}/{}'.format(version, file)
        message += "[{}]({}) ".format(version, link)
    return message, status


def check_models(device):
    """
    get different models of device info
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    if not check_codename(device):
        message = "Wrong codename!"
        status = False
        return message, status
    data = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/models/models.json").text)
    info = [i for i in data if device == i['codename']]
    if not info:
        message = "Can't find info about {}!".format(device)
        status = False
        return message, status
    for item in info:
        codename = item['codename']
        internal = item['internal_name']
        name = item['name']
        message += "*{} ({} - {}) Models:*\n".format(name, codename, internal)
        models = item['models']
        for model, model_name in models.items():
            message += "{}: {}\n".format(model, model_name)
    status = True
    return message, status


def whatis(device):
    """
    checks device name based on its codename
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    current = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "miui-updates-tracker/master/devices/names.json").text.replace(']\n}', '],')
    eol = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "miui-updates-tracker/master/EOL/names.json").text.replace('{', '')
    data = json.loads(current + eol)
    data = list(data.items())
    info = [i for i in data if device == i[0].split('_')[0]]
    if not info:
        message = "Can't find info about {}!".format(device)
        status = False
        return message, status
    for codename, details in info:
        codename = codename
        name = details[0]
        message += "`{}` is *{}*\n".format(codename, name)
    status = True
    return message, status
