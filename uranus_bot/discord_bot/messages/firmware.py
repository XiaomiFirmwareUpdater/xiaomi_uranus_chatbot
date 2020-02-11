""" Firmware messages generator """
from discord import Embed
from uranus_bot import XFU_WEBSITE


async def firmware_message(device):
    """ Generate discord message of firmware command """
    embed = Embed(title=f'**Available firmware downloads for** `{device}`')
    embed.add_field(name='Latest Firmware',
                    value=f'[Download]({XFU_WEBSITE}/firmware/{device}/)')
    embed.add_field(name='Firmware Archive',
                    value=f'[Download]({XFU_WEBSITE}/archive/firmware/{device}/)')
    return embed
