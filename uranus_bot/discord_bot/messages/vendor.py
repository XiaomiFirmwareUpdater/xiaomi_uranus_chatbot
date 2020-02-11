""" Vendor messages generator """
from discord import Embed
from uranus_bot import XFU_WEBSITE


async def vendor_message(device):
    """ Generate discord message of vendor command """
    embed = Embed(title=f'**Available vendor downloads for** `{device}`')
    embed.add_field(name='Latest Vendor',
                    value=f'[Download]({XFU_WEBSITE}/vendor/{device}/)')
    embed.add_field(name='Vendor Archive',
                    value=f'[Download]({XFU_WEBSITE}/archive/vendor/{device}/)')
    return embed
