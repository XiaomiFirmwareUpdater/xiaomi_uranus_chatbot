""" OrangeFox messages generator """
from telethon import Button

from uranus_bot.providers.custom_recovery.orangefox.orangefox import get_orangefox


async def orangefox_message(device, orangefox_data):
    """ Generate telegram message of orangefox command """
    data = await get_orangefox(device, orangefox_data)
    message = f'**Latest {data["name"]} **(`{device}`) ' \
              f'[OrangeFox](https://wiki.orangefox.tech/en/home) Builds:\n' \
              f'__Maintainer:__ {data["maintainer"]}\n'
    buttons = []
    for item in data["downloads"]:
        for file, link in item.items():
            buttons.append([Button.url(f'{file}', url=link)])
    return message, buttons


async def orangefox_inline(event, device, orangefox_data):
    """ Generate telegram result of orangefox inline query """
    builder = event.builder
    message, buttons = await orangefox_message(device, orangefox_data)
    result = builder.article(
        f'Search {device} OrangeFox recovery downloads',
        text=message,
        buttons=buttons,
        link_preview=False
    )
    return result
