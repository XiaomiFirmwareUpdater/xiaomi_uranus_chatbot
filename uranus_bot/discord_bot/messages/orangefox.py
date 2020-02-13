""" OrangeFox messages generator """
from discord import Embed

from uranus_bot.providers.custom_recovery.orangefox.orangefox import get_orangefox


async def orangefox_message(device, orangefox_data):
    """ Generate discord message of orangefox command """
    data = await get_orangefox(device, orangefox_data)
    embed = Embed(title=f'**Latest {data["name"]} (**`{device}`) **OrangeFox Builds**',
                  description=f'__Maintainer:__ {data["maintainer"]}')
    for item in data["downloads"]:
        for file, link in item.items():
            embed.add_field(name=f'{file}',
                            value=f'[Download]({link})')
    return embed
