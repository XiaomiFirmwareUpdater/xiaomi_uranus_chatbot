""" firmware messages generator """
from telethon import Button

from uranus_bot import XFU_WEBSITE


async def firmware_message(device):
    """ Generate telegram message of firmware command """
    message = f'**Available firmware downloads for** `{device}`\n'
    buttons = [
        [Button.url("Latest Firmware", f"{XFU_WEBSITE}/firmware/{device}/"),
         Button.url("Firmware Archive", f"{XFU_WEBSITE}/archive/firmware/{device}/")],
        [Button.url("XiaomiFirmwareUpdater", "https://t.me/XiaomiFirmwareUpdater")]
    ]
    return message, buttons


async def firmware_inline(event, device):
    """ Generate telegram result of firmware inline query """
    builder = event.builder
    message, buttons = await firmware_message(device)
    result = builder.article(
        f'Search {device} Firmware downloads', text=message,
        buttons=buttons, ink_preview=False
    )
    return result
