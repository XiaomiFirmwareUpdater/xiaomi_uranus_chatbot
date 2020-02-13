""" OSS messages generator """
from discord import Embed

from uranus_bot.providers.xiaomi_oss.xiaomi_oss import get_oss


async def oss_message(device):
    """ Generate discord message of oss command """
    data = await get_oss(device)
    if not data:
        return
    message = ""
    for i in data:
        message += f"**Devices:** {i.split('|')[2].strip()}\n" \
                   f"{i.split('|')[3].strip()}\n" \
                   f"**Tag:** {i.split('|')[4].strip()}\n" \
                   f"{i.split('|')[5].strip()}\n\n"
    embed = Embed(title=f"**Xiaomi OSS Kernel Releases for** `{device}`",
                  description=message)
    return embed
