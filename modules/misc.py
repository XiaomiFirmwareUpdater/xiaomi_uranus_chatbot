#!/usr/bin/env python3.7
"""Uranus Bot misc funcs"""

from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from requests import get
from .mwt import MWT

WIKI = 'https://xiaomiwiki.github.io/wiki'
XDA = 'https://www.xda-developers.com'


@MWT(timeout=60 * 60 * 12)
def arb_table():
    """
    auto get arb table from Xiaomi.eu website every 12h
    :return: img link
    """
    response = get('https://xiaomi.eu/community/link-forums/roms-download.73/')
    page = BeautifulSoup(response.content, 'html.parser')
    img = page.findAll('img', {"class": "bbImage"})[1]['src']
    return img


def unlock():
    """
    device unlock info
    :returns message - telegram message string
    """
    message = "Unlocking bootloader guide and tool"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("How to Unlock the bootloader", f'{WIKI}/Unlock_the_bootloader.html'),
         InlineKeyboardButton("Mi Unlock Tool", f'http://en.miui.com/unlock/download_en.html')]
    ])
    return message, reply_markup


def tools():
    """
    various tools for Xiaomi devices
    :returns message - telegram message string
    """
    url = f'{WIKI}/Tools_for_Xiaomi_devices.html'
    message = "Tools for Xiaomi devices"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Mi Flash Tool", f'{url}#miflash-by-xiaomi'),
         InlineKeyboardButton("MiFlash Pro", f'{url}#miflash-pro-by-xiaomi'),
         InlineKeyboardButton("Mi Unlock Tool", f'{url}#miunlock-by-xiaomi')],
        [InlineKeyboardButton("XiaomiTool", f'{url}#xiaomitool-v2-by-francesco-tescari'),
         InlineKeyboardButton("XiaomiADB", f'{url}#xiaomiadb-by-francesco-tescari'),
         InlineKeyboardButton("Unofficial MiUnlock", f'{url}#miunlocktool-by-francesco-tescari')],
        [InlineKeyboardButton("Xiaomi ADB/Fastboot Tools", f'{url}#xiaomi-adbfastboot-tools-by-saki_eu'),
         InlineKeyboardButton("More Tools", f'{url}')]
    ])
    return message, reply_markup


def arb():
    """
    Anti-Rollback Protection unlock info
    :returns message - telegram message string
    """
    caption = f'[About Anti-Rollback Protection]' \
              f'({WIKI}/About_Anti-Rollback_Protection.html)\n' \
              f'[Xiaomi’s Anti-Rollback Protection Explained]' \
              f'({XDA}/xiaomi-anti-rollback-protection-brick-phone/)\n'
    photo = arb_table()
    return caption, photo


def guides():
    """
    various useful guides
    :returns message - telegram message string
    """
    message = "Guides for Xiaomi devices"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Flashing official ROMs", f'{WIKI}/Flash_official_ROMs.html')],
        [InlineKeyboardButton("Flashing TWRP & custom ROMs", f'{WIKI}/Flash_TWRP_and_custom_ROMs.html')],
        [InlineKeyboardButton("Fix notifications on MIUI", f'{WIKI}/Fix_notifications_on_MIUI.html')],
        [InlineKeyboardButton("Disable MIUI Ads 1", f'{WIKI}/Disable_ads_in_MIUI.html'),
         InlineKeyboardButton("Disable MIUI Ads 2", f'{XDA}/xiaomi-miui-ads-hamper-user-experience/')]
    ])
    return message, reply_markup
