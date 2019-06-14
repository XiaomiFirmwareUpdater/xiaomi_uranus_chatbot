#!/usr/bin/env python3.7
"""Uranus Bot misc funcs"""

WIKI = 'https://xiaomiwiki.github.io/wiki'
XDA = 'https://www.xda-developers.com'


def unlock():
    """
    device unlock info
    :returns message - telegram message string
    """
    message = f'[How to Unlock the bootloader]' \
              f'({WIKI}/Unlock_the_bootloader.html)\n' \
              f'[Mi Unlock Tool](http://en.miui.com/unlock/download_en.html)'
    return message


def tools():
    """
    various tools for Xiaomi devices
    :returns message - telegram message string
    """
    url = f'{WIKI}/Tools_for_Xiaomi_devices.html'
    message = f'*Official Tools*\n' \
        f'[Mi Flash Tool]({url}#miflash-by-xiaomi)\n' \
        f'[MiFlash Pro]({url}#miflash-pro-by-xiaomi)\n' \
        f'[Mi Unlock Tool]({url}#miunlock-by-xiaomi)\n' \
        '\n*Unofficial Tools*\n' \
        f'[XiaomiTool]({url}#xiaomitool-v2-by-francesco-tescari)\n' \
        f'[XiaomiADB]({url}#xiaomiadb-by-francesco-tescari)\n' \
        f'[MiUnlockTool]({url}#miunlocktool-by-francesco-tescari)\n' \
        f'[Xiaomi ADB/Fastboot Tools]({url}#xiaomi-adbfastboot-tools-by-saki_eu)\n' \
        f'\n *More Tools*: [Here]({url})'
    return message


def arb():
    """
    Anti-Rollback Protection unlock info
    :returns message - telegram message string
    """
    caption = f'[About Anti-Rollback Protection]' \
              f'({WIKI}/About_Anti-Rollback_Protection.html)\n' \
              f'[Xiaomi’s Anti-Rollback Protection Explained]' \
              f'({XDA}/xiaomi-anti-rollback-protection-brick-phone/)\n'
    photo = 'https://i.imgur.com/YsPIyyr.png'
    return caption, photo


def guides():
    """
    various useful guides
    :returns message - telegram message string
    """
    message = f'[Flashing official ROMs]' \
        f'({WIKI}/Flash_official_ROMs.html)\n' \
        f'[Flashing TWRP & custom ROMs]({WIKI}/Flash_TWRP_and_custom_ROMs.html)\n' \
        f'*Disable ads in MIUI*: [Wiki]({WIKI}/Disable_ads_in_MIUI.html) - ' \
        f'[XDA]({XDA}/xiaomi-miui-ads-hamper-user-experience/)\n' \
        f'[Fix notifications on MIUI]({WIKI}/Fix_notifications_on_MIUI.html)\n'
    return message
