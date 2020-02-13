"""Xiaomi OSS info scraper"""

from aiohttp import ClientSession

from uranus_bot.providers.utils.utils import fetch


async def get_oss(device):
    """ Get OSS kernel of a devce by its name """
    async with ClientSession() as session:
        raw = await fetch(session, f'https://raw.githubusercontent.com/MiCode/'
                                   f'Xiaomi_Kernel_OpenSource/README/README.md')
        info = list(raw.splitlines())
        data = [i for i in info if device in i]
        return data if data else None
