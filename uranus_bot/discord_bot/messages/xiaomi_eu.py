""" Xiaomi.eu command handler """
from discord import Embed

from uranus_bot.providers.xiaomi_eu.xiaomi_eu import get_eu


async def eu_message(device, eu_data, devices):
    """ Generate discord message of eu command """
    data = await get_eu(device, eu_data, devices)
    if not data:
        return
    name = devices[device][0]
    embed = Embed(title=f'**{name}  (**`{device}`**) **latest Xiaomi.eu ROMs:**')
    for version, link in data.items():
        embed.add_field(name=f'{version}', value=f'[Download]({link})')
    return embed
