"""Bootloader unlock info provider"""

from uranus_bot.providers.misc import WIKI


async def get_unlock_guides():
    """device unlock guides"""
    return [{
        "How to Unlock the bootloader": f"{WIKI}/Unlock_the_bootloader.html",
        "Mi Unlock Tool": "http://en.miui.com/unlock/download_en.html"
    }]
