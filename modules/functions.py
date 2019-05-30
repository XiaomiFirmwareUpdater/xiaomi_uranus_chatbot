#!/usr/bin/env python3.7
"""Xiaomi Helper Bot general commands"""

import json
from requests import get

CODENAMES = get(
    "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
    "xiaomi_devices/codenames/codenames.json").json()


def check_codename(codename):
    """check if codename is correct"""
    codename = codename.lower()
    found = False
    if [i for i in CODENAMES if codename == i.lower()]:
        found = True
    elif [i for i in CODENAMES if codename == i.split('_')[0].lower()]:
        found = True
    return found


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
    global_stable = [i for i in stable if i['type'] == 'Global']
    china_stable = [i for i in stable if i['type'] == 'China']
    global_weekly = [i for i in weekly if i['type'] == 'Global']
    china_weekly = [i for i in weekly if i['type'] == 'China']

    def gen_link(data):
        version = data['versions']['miui']
        file = '_'.join(data['filename'].split('_')[2:])
        link = 'http://bigota.d.miui.com/{}/{}'.format(version, file)
        reply = "[{}]({}) ".format(version, link)
        return reply

    message = '*Available Stable ROMs:*\n'
    if global_stable:
        message += '_Global:_\n'
        for i in global_stable:
            message += gen_link(i)
    if china_stable:
        message += '\n_China:_\n'
        for i in china_stable:
            message += gen_link(i)
    message += '\n*Available Weekly ROMs:*\n'
    if global_weekly:
        message += '_Global:_\n'
        for i in global_weekly:
            message += gen_link(i)
    if china_weekly:
        message += '\n_China:_\n'
        for i in china_weekly:
            message += gen_link(i)
    return message, status


def check_models(device):
    """
    get different models of device info
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    if check_codename(device) is False:
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
    if check_codename(device) is False:
        message = "Wrong codename!"
        status = False
        return message, status
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/names/names.json'
    devices = get(url).json()
    info = {i: devices[i] for i in devices if device.lower() == i.lower()}
    if not info:
        message = "Can't find info about {}!".format(device)
        status = False
        return message, status
    for key, value in info.items():
        codename = key
        name = value
        message += "`{}` is *{}*\n".format(codename, name)
    status = True
    return message, status


def specs(device):
    """
    Get device specs based on its codename
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    if check_codename(device) is False:
        message = "Wrong codename!"
        status = False
        return message, status
    data = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/xiaomi_devices" +
        "/gsmarena/devices.json").json()
    try:
        info = [i for i in data if device == i['codename']][0]
    except IndexError:
        info = {}
    if not info:
        message = "Can't find info about {}!".format(device)
        status = False
        return message, status
    name = info['name']
    url = info['url']
    details = info['specs']
    device_status = details['Launch'][0]['Status']
    network = details['Network'][0]['Technology']
    weight = details['Body'][0]['Weight']
    display = details['Display'][0]['Type'] + '\n' + details['Display'][0]['Size'] + '\n' +\
              details['Display'][0]['Resolution']
    chipset = details['Platform'][0]['Chipset'] + '\n' + details['Platform'][0]['CPU'] + '\n' +\
              details['Platform'][0]['GPU']
    memory = details['Memory'][0]['Internal']
    main_cam = details['Main Camera'][0]
    try:
        main_cam = main_cam['Triple']
    except KeyError:
        try:
            main_cam = main_cam['Dual']
        except KeyError:
            try:
                main_cam = main_cam['Single']
            except KeyError:
                pass
    front_cam = details['Selfie camera'][0]
    try:
        front_cam = front_cam['Triple']
    except KeyError:
        try:
            front_cam = front_cam['Dual']
        except KeyError:
            try:
                front_cam = front_cam['Single']
            except KeyError:
                pass
    jack = details['Sound'][0]['3.5mm jack ']
    usb = details['Comms'][0]['USB']
    sensors = details['Features'][0]['Sensors']
    battery = details['Battery'][0]['info']
    message += "[{}]({}) - *{}*\n*Status*: {}\n*Network:* {}\n*Weight*: {}\n" \
               "*Display*:\n{}\n*Chipset*:\n{}\n*Memory*: {}\n" \
               "*Rear Camera*: {}\n*Front Camera*: {}\n*3.5mm jack*: {}\n" \
               "*USB*: {}\n*Sensors*: {}\n*Battery*: {}" \
        .format(name, url, device, device_status, network, weight, display, chipset,
                memory, main_cam, front_cam, jack, usb, sensors, battery)
    try:
        charging = details['Battery'][0]['Charging']
        message += "\n*Charging*: {}" \
            .format(charging)
    except KeyError:
        pass
    status = True
    return message, status
