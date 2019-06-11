#!/usr/bin/env python3.7
"""Xiaomi Helper Bot general commands"""

from bs4 import BeautifulSoup
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


def set_branch(version):
    """
    checks MIUI branch based on MIUI version
    :param version: MIUI version, stable/weekly
    :return: branch
    """
    if 'V' in version:
        branch = 'Stable'
    else:
        branch = 'Weekly'
    return branch


def set_region(file):
    """
    sets MIUI ROM region from ROM file
    :param file: MIUI file, fastboot/recovery
    :return: region
    """
    if 'eea_global' in file or 'EU' in file:
        region = 'EEA Global'
    elif 'in_global' in file or 'IN' in file:
        region = 'India'
    elif 'ru_global' in file or 'RU' in file:
        region = 'Russia'
    elif 'global' in file or 'MI' in file:
        region = 'Global'
    else:
        region = 'China'
    return region


def load_fastboot_data(device):
    """
    load latest fasboot ROMs data form MIUI tracker json files
    :argument device - Xiaomi device codename
    :returns data - a list with merged stable, weekly, current, and EOL data
    """
    stable_roms = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "stable_fastboot/stable_fastboot.json").json()
    weekly_roms = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "weekly_fastboot/weekly_fastboot.json").json()
    eol_stable_roms = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "stable_fastboot/stable_fastboot.json").json()
    eol_weekly_roms = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "weekly_fastboot/weekly_fastboot.json").json()
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
    stable_roms = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "stable_recovery/stable_recovery.json").json()
    weekly_roms = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "weekly_recovery/weekly_recovery.json").json()
    eol_stable_roms = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "stable_recovery/stable_recovery.json").json()
    eol_weekly_roms = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "weekly_recovery/weekly_recovery.json").json()
    stable_roms = [i for i in stable_roms
                   if device == i['codename'].split('_')[0] and i['version']]
    weekly_roms = [i for i in weekly_roms
                   if device == i['codename'].split('_')[0] and i['version']]
    eol_stable_roms = [i for i in eol_stable_roms
                       if device == i['codename'].split('_')[0] and i['version']]
    eol_weekly_roms = [i for i in eol_weekly_roms
                       if device == i['codename'].split('_')[0] and i['version']]
    data = stable_roms + weekly_roms + eol_stable_roms + eol_weekly_roms
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
        rom_type = set_branch(version)
        message += f"Latest {name} {rom_type} ROM:\n" \
                   f"*Version:* `{version}` \n" \
                   f"*Android:* {android} \n" \
                   f"*Download*: [Here]({download}) \n\n"
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
        rom_type = set_branch(version)
        message += f"Latest {name} {rom_type} ROM:\n" \
                   f"*Version:* `{version}` \n" \
                   f"*Android:* {android} \n"
        message += f"*Download*: [Here]({download}) \n\n"
    return message, status


def gen_fw_link(device):
    """
    generate latest firmware links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    devices = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/devices.json").json()
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
        rom_type = set_branch(version)
        file = i['filename']
        region = set_region(file)
        message += f"Latest {region} {rom_type}: `{version}`\n"
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
        message += f"{item.strip()}\n"
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


def history(device):
    """
    get all released MIUI rom for device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    devices = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomifirmwareupdater.github.io/master/data/devices.json").json()
    status = None
    if not [i for i in devices if device == i['codename'].split('_')[0]]:
        message = "Wrong codename!"
        return message, status
    message = '*Available Stable ROMs:*\n'
    data = fetch_fw_data(device)
    message += data
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
    data = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/models/models.json").json()
    info = [i for i in data if device == i['codename']]
    if not info:
        message = f"Can't find info about {device}!"
        status = False
        return message, status
    for item in info:
        codename = item['codename']
        internal = item['internal_name']
        name = item['name']
        message += f"*{name} ({codename} - {internal}) Models:*\n"
        models = item['models']
        for model, model_name in models.items():
            message += f"{model}: {model_name}\n"
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
        message = f"Can't find info about {device}!"
        status = False
        return message, status
    for key, value in info.items():
        codename = key
        name = value
        message += f"`{codename}` is *{name}*\n"
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
        message = f"Can't find info about {device}!"
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
    message += f"[{name}]({url}) - *{device}*\n*Status*: {device_status}\n*Network:* {network}\n" \
               f"*Weight*: {weight}\n*Display*:\n{display}\n*Chipset*:\n{chipset}\n" \
               f"*Memory*: {memory}\n*Rear Camera*: {main_cam}\n*Front Camera*: {front_cam}\n" \
               f"*3.5mm jack*: {jack}\n*USB*: {usb}\n*Sensors*: {sensors}\n*Battery*: {battery}"
    try:
        charging = details['Battery'][0]['Charging']
        message += f"\n*Charging*: {charging}"
    except KeyError:
        pass
    status = True
    return message, status


def fetch_vendor(device):
    """
    generate latest firmware links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    if check_codename(device) is False:
        message = "Wrong codename!"
        status = False
        return message, status
    status = None
    message = ''

    def fetch(data, branch):
        reply = ''
        for i in data:
            for codename, version in i.items():
                version = version.split('_')[1]
                url = 'https://github.com/TryHardDood/mi-vendor-updater/releases/' \
                    f'tag/{codename}-{branch}'
                response = get(url)
                page = BeautifulSoup(response.content, 'html.parser')
                links = [i for i in page.findAll('a') if version in str(i)]
                if not links:
                    continue
                link = BeautifulSoup(str(links), 'html.parser')
                file = link.a['href'].split('/')[-1]
                rom_type = set_branch(version)
                region = set_region(file)
                reply += f"{region} {rom_type}: [{version}](https://github.com{link.a['href']})\n"
        return reply
    stable = get('https://raw.githubusercontent.com/TryHardDood/' +
                 'mi-vendor-updater/master/stable.json').json()
    stable = [i for i in stable if device in str(i)]
    if not stable:
        message = f"Can't find info about {device}!"
        status = False
        return message, status
    message += fetch(stable, 'stable')
    weekly = get('https://raw.githubusercontent.com/TryHardDood/' +
                 'mi-vendor-updater/master/weekly.json').json()
    weekly = [i for i in weekly if device in str(i)]
    if weekly:
        message += fetch(weekly, 'weekly')
    message += '@MIUIVendorUpdater'
    return message, status
