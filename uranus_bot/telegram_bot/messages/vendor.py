""" vendor messages generator """
from telethon import Button

from uranus_bot import XFU_WEBSITE
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def vendor_message(device, codenames_names, locale):
    """ Generate telegram message of vendor command """
    message = LOCALIZE.get_text(locale, "vendor_message").replace(
        "{device}", device).replace("{codenames_names[device]}", codenames_names[device])
    buttons = [
        [Button.url(LOCALIZE.get_text(locale, "latest_vendor"),
                    f"{XFU_WEBSITE}/vendor/{device}/"),
         Button.url(LOCALIZE.get_text(locale, "archive_vendor"),
                    f"{XFU_WEBSITE}/archive/vendor/{device}/")],
        [Button.url(LOCALIZE.get_text(locale, "MIUIVendorUpdater"),
                    "https://t.me/MIUIVendorUpdater")]
    ]
    return message, buttons


async def vendor_inline(event, device, codenames_names, locale):
    """ Generate telegram result of vendor inline query """
    builder = event.builder
    message, buttons = await vendor_message(device, codenames_names, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "vendor_inline").replace(
            "{device}", device).replace(
            "{codenames_names[device]}", codenames_names[device]),
        text=message,
        buttons=buttons, link_preview=False)
    return result


async def vendor_update_message(codename, update, locale):
    """ Generate telegram message of vendor update """
    message = LOCALIZE.get_text(locale, "vendor_update").replace("{codename}", codename)
    buttons = [
        [Button.url(f"{update}",
                    f"{XFU_WEBSITE}/vendor/{codename}/")],
        [Button.url(LOCALIZE.get_text(locale, "MIUIVendorUpdater"),
                    "https://t.me/MIUIVendorUpdater")]
    ]
    return message, buttons
