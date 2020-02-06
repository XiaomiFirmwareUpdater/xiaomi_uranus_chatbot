#!/usr/bin/env python3.7
"""Xiaomi devices info"""
from uuid import uuid4

from requests import get
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode

from .extras import check_codename, check_name
from .mwt import MWT


@MWT(timeout=60 * 60 * 6)
def fetch_models():
    """
    fetches models data every 6h
    :return: devices
    """
    devices = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/models/models.json").json()
    return devices


@MWT(timeout=60 * 60 * 6)
@check_codename(markup=False)
def check_models(device, inline=False):
    """
    get different models of device info
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    """
    message = ''
    data = fetch_models()
    info = [i for i in data if device == i['codename']]
    if not info:
        return ""
    for item in info:
        codename = item['codename']
        internal = item['internal_name']
        name = item['name']
        message += f"*{name} ({codename} - {internal}) Models:*\n"
        models = item['models']
        for model, model_name in models.items():
            message += f"{model}: {model_name}\n"
    if inline:
        results = [InlineQueryResultArticle(
            id=uuid4(),
            title=f"Search {device} device models",
            input_message_content=InputTextMessageContent(
                message, parse_mode=ParseMode.MARKDOWN))]
        return results
    else:
        return message


@MWT(timeout=60 * 60 * 6)
def fetch_codenames():
    """
    fetches codenames data every 6h
    :return: devices
    """
    devices = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/names/names.json").json()
    return devices


@MWT(timeout=60 * 60 * 6)
@check_codename(markup=False)
def whatis(device, inline=False):
    """
    checks device name based on its codename
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    """
    message = ''
    devices = fetch_codenames()
    info = {i: devices[i] for i in devices if device.lower() == i.lower()}
    if not info:
        return ""
    for key, value in info.items():
        codename = key
        name = value
        message += f"`{codename}` is *{name}*\n"
    if inline:
        results = [InlineQueryResultArticle(
            id=uuid4(),
            title=f"Search {device} device name",
            input_message_content=InputTextMessageContent(
                message, parse_mode=ParseMode.MARKDOWN))]
        return results
    else:
        return message


@MWT(timeout=60 * 60 * 6)
@check_name
def get_codename(name):
    """
    checks device codename based on its name
    :argument name - Xiaomi device name
    :returns message - telegram message string
    """
    message = ''
    devices = fetch_codenames()
    devices = {i: devices[i] for i in devices if i.count('_') < 2}
    info = {i: devices[i] for i in devices if str(devices[i].lower()).startswith(name.lower())}
    if not info:
        return ""
    if len(info) > 7:
        message = f"{name} is too general! Please be more specific."
        return message
    for key, value in info.items():
        codename = key
        name = value
        message += f"*{name}* is `{codename}`\n"
    return message
