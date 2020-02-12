""" vendor messages generator """
from telethon import Button

from uranus_bot import XFU_WEBSITE


async def vendor_message(device, codenames_names):
    """ Generate telegram message of vendor command """
    message = f'**Available vendor downloads for {codenames_names[device]}** (`{device}`)\n'
    buttons = [
        [Button.url("Latest Vendor", f"{XFU_WEBSITE}/vendor/{device}/"),
         Button.url("Vendor Archive", f"{XFU_WEBSITE}/archive/vendor/{device}/")],
        [Button.url("MIUIVendorUpdater", "https://t.me/MIUIVendorUpdater")]
    ]
    return message, buttons


async def vendor_inline(event, device, codenames_names):
    """ Generate telegram result of vendor inline query """
    builder = event.builder
    message, buttons = await vendor_message(device, codenames_names)
    result = builder.article(
        f'Search {codenames_names[device]}** (`{device}`) Vendor downloads', text=message,
        buttons=buttons, link_preview=False)
    return result
