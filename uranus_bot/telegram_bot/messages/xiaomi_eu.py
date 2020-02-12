""" Xiaomi.eu messages generator """
from telethon import Button

from uranus_bot.providers.xiaomi_eu.xiaomi_eu import get_eu


async def eu_message(device, eu_data, devices):
    """ Generate telegram message of eu command """
    data = await get_eu(device, eu_data, devices)
    if not data:
        return
    name = devices[device][0]
    message = f'**{name} (**`{device}`**) latest Xiaomi.eu ROMs:**\n'
    buttons = []
    for version, link in data.items():
        buttons.append([Button.url(f"{version}", url=link)])
    return message, buttons


async def eu_inline(event, device, eu_data, devices):
    """ Generate telegram result of eu inline query """
    try:
        message, buttons = await eu_message(device, eu_data, devices)
    except TypeError:
        return
    name = devices[device][0]
    builder = event.builder
    result = builder.article(
        f'Search {name} ({device}) Xiaomi.eu downloads',
        text=message,
        buttons=buttons,
        link_preview=False
    )
    return result
