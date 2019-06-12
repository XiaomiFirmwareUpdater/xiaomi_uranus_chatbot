#!/usr/bin/env python3.7
"""Xiaomi devices info"""

from requests import get
from .extras import check_codename, check_name
from .mwt import MWT


@MWT(timeout=60*60*6)
def fetch_models():
    """
    fetches models data every 6h
    :return: devices
    """
    devices = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/models/models.json").json()
    return devices


@MWT(timeout=60*60*6)
@check_codename
def check_models(device):
    """
    get different models of device info
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    data = fetch_models()
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


@MWT(timeout=60*60*6)
def fetch_codenames():
    """
    fetches codenames data every 6h
    :return: devices
    """
    devices = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/names/names.json").json()
    return devices


@MWT(timeout=60*60*6)
@check_codename
def whatis(device):
    """
    checks device name based on its codename
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    devices = fetch_codenames()
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


@MWT(timeout=60*60*6)
@check_name
def get_codename(name):
    """
    checks device codename based on its name
    :argument name - Xiaomi device name
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    message = ''
    devices = fetch_codenames()
    devices = {i: devices[i] for i in devices if '_' not in i}
    info = {i: devices[i] for i in devices if str(devices[i].lower()).startswith(name.lower())}
    if not info:
        message = f"Can't find info about {name}!"
        status = False
        return message, status
    if len(info) > 7:
        message = f"{name} is too general! Please be more specific."
        status = False
        return message, status
    for key, value in info.items():
        codename = key
        name = value
        message += f"*{name}* is `{codename}`\n"
    status = True
    return message, status
