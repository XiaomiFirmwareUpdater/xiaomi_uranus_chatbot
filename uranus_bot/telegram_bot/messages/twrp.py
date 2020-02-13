""" TWRP messages generator """
from telethon import Button

from uranus_bot.providers.custom_recovery.twrp.twrp import get_twrp


async def twrp_message(device, twrp_data):
    """ Generate telegram message of twrp command """
    data = await get_twrp(device, twrp_data)
    message = f'**Latest TWRP for {data["name"]}:**\n' \
              f'**Updated:** {data["date"]}\n'
    buttons = [
        [Button.url(f'{data["dl_file"]} - {data["size"]}', url=data["dl_link"])]
    ]
    return message, buttons


async def twrp_inline(event, device, twrp_data):
    """ Generate telegram result of twrp inline query """
    builder = event.builder
    message, buttons = await twrp_message(device, twrp_data)
    result = builder.article(
        f'Search {device} TWRP downloads',
        text=message,
        buttons=buttons,
        link_preview=False
    )
    return result
