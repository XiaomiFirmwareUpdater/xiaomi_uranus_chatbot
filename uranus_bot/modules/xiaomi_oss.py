#!/usr/bin/env python3.7
"""Xiaomi devices oss checker"""

from requests import get
from .mwt import MWT


@MWT(timeout=60 * 60 * 6)
def oss(device):
    """
    get latest oss kernel for a device from MIUI Mi Code repo
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    """
    info = list(get(
        "https://raw.githubusercontent.com/MiCode/Xiaomi_Kernel_OpenSource/" +
        "README/README.md").text.splitlines())
    data = [i for i in info if device in i]
    message = ''
    if not data:
        return ""
    for i in data:
        name = i.split('|')[2].strip()
        android = i.split('|')[3].strip()
        tag = i.split('|')[4].strip()
        link = i.split('|')[5].strip()
        message += f"*Devices:* {name}\n" \
                   f"{android}\n" \
                   f"*Tag:* {tag}\n" \
                   f"{link}\n\n"
    return message
