""" firmware messages generator """
from telethon import Button

from uranus_bot import XFU_WEBSITE
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def firmware_message(device, codenames_names, locale):
    """ Generate telegram message of firmware command """
    message = f'**{LOCALIZE.get_text(locale, "available_firmware")} {codenames_names[device]}** ' \
              f'(`{device}`)\n'
    buttons = [
        [Button.url(LOCALIZE.get_text(locale, "latest_firmware"),
                    f"{XFU_WEBSITE}/firmware/{device}/"),
         Button.url(LOCALIZE.get_text(locale, "archive_firmware"),
                    f"{XFU_WEBSITE}/archive/firmware/{device}/")],
        [Button.url(LOCALIZE.get_text(locale, "XiaomiFirmwareUpdater"),
                    "https://t.me/XiaomiFirmwareUpdater")]
    ]
    return message, buttons


async def firmware_inline(event, device, codenames_names, locale):
    """ Generate telegram result of firmware inline query """
    builder = event.builder
    message, buttons = await firmware_message(device, codenames_names, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "firmware_inline").replace(
            "{codenames_names[device]}", codenames_names[device]).replace("{device}", device),
        text=message, buttons=buttons, link_preview=False
    )
    return result


async def firmware_update_message(codename, update, locale):
    """ Generate telegram message of firmware update """
    message = LOCALIZE.get_text(locale, "firmware_update").replace("{codename}", codename)
    buttons = [Button.url(f"{update}",
                          f"{XFU_WEBSITE}/firmware/{codename}/")]
    return message, buttons
