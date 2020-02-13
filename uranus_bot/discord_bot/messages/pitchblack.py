""" PitchBlack messages generator """
from discord import Embed

from uranus_bot.providers.custom_recovery.pitchblack.pitchblack import get_pitchblack


async def pitchblack_message(device, pitchblack_data):
    """ Generate discord message of pitchblack command """
    data = await get_pitchblack(device, pitchblack_data)
    embed = Embed(title=f'**Latest PitchBlack Build for **`{device}`')
    for file, link in data.items():
        embed.add_field(name=f'{file}', value=f'[Download]({link})')
    return embed
