""" OrangeFox messages generator """
from telethon import Button

from uranus_bot.providers.custom_recovery.orangefox.orangefox import get_orangefox
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def orangefox_message(device, locale):
    """ Generate telegram message of orangefox command """
    data = await get_orangefox(device)
    if not data:
        return
    message = LOCALIZE.get_text(locale, "orangefox_message").replace(
        "{data['name']}", data['name']).replace("{device}", device).replace(
        "{data['maintainer']}", data['maintainer'])
    buttons = []
    for item in data["downloads"]:
        for file, link in item.items():
            buttons.append([Button.url(f'{file}', url=link)])
    return message, buttons


async def orangefox_inline(event, device, locale):
    """ Generate telegram result of orangefox inline query """
    builder = event.builder
    message, buttons = await orangefox_message(device, orangefox_data, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "orangefox_inline").replace("{device}", device),
        text=message,
        buttons=buttons,
        link_preview=False
    )
    return result
