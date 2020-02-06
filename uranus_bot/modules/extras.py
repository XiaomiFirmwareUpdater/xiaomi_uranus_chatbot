#!/usr/bin/env python3.7
"""Uranus Bot helper funcs"""
from requests import get
from uranus_bot.modules.mwt import MWT


@MWT(timeout=60 * 60)
def load_codenames():
    """
    load codenames data from XFU repo
    :return: list of codenames
    """
    codenames = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/codenames/codenames.json").json()
    return codenames


def check_codename(devices=load_codenames(), markup=False):
    """check if codename is correct"""

    def _check_codename(function):
        def wrapper(*args, **kwargs):
            codename = args[0].lower()
            matched_devices = [i for i in devices if codename.split('_')[0] == i] \
                              or [i for i in devices if codename == i.lower()]
            if markup:
                if matched_devices:
                    try:
                        message, reply_markup = function(*args, **kwargs)
                    except ValueError:  # workaround for inline
                        results = function(*args, **kwargs)
                        return results
                else:
                    message = ""
                    reply_markup = None
                return message, reply_markup
            if matched_devices:
                message = function(*args, **kwargs)
            else:
                message = ""
            return message

        return wrapper

    return _check_codename


@MWT(timeout=60 * 60)
def load_names():
    """
    load names data from XFU repo
    :return: list of names
    """
    names = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/names/names.json").json()
    names = list(names.values())
    return names


def check_name(func):
    """check if codename is correct"""

    def wrapper(*args, **kwargs):
        name = args[0].lower()
        names = load_names()
        if [i for i in names if name in i.lower()]:
            message = func(*args, **kwargs)
        else:
            message = ""
        return message

    return wrapper


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


def set_region(filename, version):
    """
    sets MIUI ROM region from ROM file
    :param filename: MIUI file, fastboot/recovery
    :param version: MIUI version
    :return: region
    """
    if 'eea_global' in filename or 'EU' in version:
        region = 'EEA'
    elif 'id_global' in filename or 'ID' in version:
        region = 'Indonesia'
    elif 'in_global' in filename or 'IN' in version:
        region = 'India'
    elif 'ru_global' in filename or 'RU' in version:
        region = 'Russia'
    elif 'global' in filename or 'MI' in version:
        region = 'Global'
    else:
        region = 'China'
    return region
