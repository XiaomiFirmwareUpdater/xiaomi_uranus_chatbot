""" Xiaomi.eu messages generator """
from telethon import Button

from uranus_bot.providers.xiaomi_eu.xiaomi_eu import get_eu
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def eu_message(device, eu_data, devices, locale):
    """ Generate telegram message of eu command """
    data = await get_eu(device, eu_data, devices)
    if not data:
        return
    name = devices[device][0]
    message = LOCALIZE.get_text(locale, "eu_message").replace(
        "{name}", name).replace("{device}", device)
    buttons = []
    for version, link in data.items():
        buttons.append([Button.url(f"{version}", url=link)])
    return message, buttons


async def eu_inline(event, device, eu_data, devices, locale):
    """ Generate telegram result of eu inline query """
    try:
        message, buttons = await eu_message(device, eu_data, devices, locale)
    except TypeError:
        return
    name = devices[device][0]
    builder = event.builder
    result = builder.article(
        LOCALIZE.get_text(locale, eu_inline).replace(
            "{name}", name).replace("{device}", device),
        text=message, buttons=buttons,
        link_preview=False
    )
    return result
