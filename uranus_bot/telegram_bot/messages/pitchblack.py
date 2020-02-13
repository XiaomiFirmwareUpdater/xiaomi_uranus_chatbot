""" PitchBlack messages generator """
from telethon import Button

from uranus_bot.providers.custom_recovery.pitchblack.pitchblack import get_pitchblack


async def pitchblack_message(device, pitchblack_data):
    """ Generate telegram message of pitchblack command """
    data = await get_pitchblack(device, pitchblack_data)
    message = f'**Latest [PitchBlack](https://pbrp.ml) Build for **`{device}`:\n'
    buttons = []
    for file, link in data.items():
        buttons.append([Button.url(f'{file}', url=link)])
    return message, buttons


async def pitchblack_inline(event, device, pitchblack_data):
    """ Generate telegram result of pitchblack inline query """
    builder = event.builder
    message, buttons = await pitchblack_message(device, pitchblack_data)
    result = builder.article(
        f'Search {device} PitchBlack downloads',
        text=message, buttons=buttons,
        link_preview=False
    )
    return result
