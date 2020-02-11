""" TWRP messages generator """
from telethon import Button
from telethon.tl import custom

from uranus_bot.providers.custom_recovery.twrp.twrp import get_twrp
from uranus_bot.telegram_bot.tg_bot import PROVIDER


async def generate_message(data):
    """ Generate telegram message text """
    return f'**Latest TWRP for {data["name"]}:**\n' \
           f'**Updated:** {data["date"]}\n'


async def twrp_message(device):
    """ Generate telegram message of twrp command """
    data = await get_twrp(PROVIDER.twrp_data, device)
    if not data:
        return None, None
    message = await generate_message(data)
    buttons = [
        [Button.url(f'{data["dl_file"]} - {data["size"]}', url=data["dl_link"])]
    ]
    return message, buttons


async def twrp_inline(event, device):
    """ Generate telegram result  of twrp inline query """
    data = get_twrp(PROVIDER.twrp_data, device)
    if not data:
        return None
    builder = event.builder
    message = await generate_message(data)
    result = builder.article(
        f'Search {device} TWRP downloads',
        text=message,
        buttons=custom.Button.url(f'{data["dl_file"]} - {data["size"]}', data["dl_link"]),
        link_preview=False
    )
    return result
