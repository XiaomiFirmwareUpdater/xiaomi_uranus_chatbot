#!/usr/bin/env python3.7
"""Xiaomi devices gsmarena info"""
# pylint: disable=too-many-locals

from requests import get

from uranus_bot.modules.extras import check_codename
from uranus_bot.modules.mwt import MWT


@check_codename(markup=False)
@MWT(timeout=60 * 60 * 6)
def specs(device):
    """
    Get device specs based on its codename
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    """
    message = ''
    data = get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/xiaomi_devices" +
        "/gsmarena/devices.json").json()
    try:
        info = [i for i in data if device == i['codename']][0]
    except IndexError:
        return ""
    name = info['name']
    url = info['url']
    details = info['specs']
    device_status = details['Launch'][0]['Status']
    network = details['Network'][0]['Technology']
    weight = details['Body'][0]['Weight']
    display = details['Display'][0]['Type'] + '\n' + details['Display'][0]['Size'] + '\n' + \
              details['Display'][0]['Resolution']
    chipset = details['Platform'][0]['Chipset'] + '\n' + details['Platform'][0]['CPU'] + '\n' + \
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
    message += f"[{name}]({url}) - *{device}*\n" \
               f"*Status*: {device_status}\n" \
               f"*Network:* {network}\n" \
               f"*Weight*: {weight}\n" \
               f"*Display*:\n{display}\n" \
               f"*Chipset*:\n{chipset}\n" \
               f"*Memory*: {memory}\n" \
               f"*Rear Camera*: {main_cam}\n" \
               f"*Front Camera*: {front_cam}\n" \
               f"*3.5mm jack*: {jack}\n" \
               f"*USB*: {usb}\n" \
               f"*Sensors*: {sensors}\n" \
               f"*Battery*: {battery}"
    try:
        charging = details['Battery'][0]['Charging']
        message += f"\n*Charging*: {charging}"
    except KeyError:
        pass
    return message
