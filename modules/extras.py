#!/usr/bin/env python3.7
"""Uranus Bot helper funcs"""
from requests import get
from .mwt import MWT


@MWT(timeout=60*60)
def load_codenames():
    """
    load codenames data from XFU repo
    :return:
    """
    codenames = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/" +
        "xiaomi_devices/codenames/codenames.json").json()
    return codenames


def check_codename(func):
    """check if codename is correct"""
    def wrapper(*args, **kwargs):
        codename = args[0].lower()
        status = False
        codenames = load_codenames()
        if [i for i in codenames if codename == i.lower()]:
            status = True
        elif [i for i in codenames if codename == i.split('_')[0].lower()]:
            status = True
        if status is True:
            message, status = func(*args, **kwargs)
        else:
            message = "Wrong codename!"
        return message, status
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
