"""Xiaomi devices info grabbers"""
# import asyncio
import json

import yaml
from aiohttp import ClientSession

from uranus_bot.providers.utils.utils import fetch

GITHUB_ORG = "https://raw.githubusercontent.com/XiaomiFirmwareUpdater"


async def load_firmware_codenames():
    """
    fetch Xiaomi devices that has firmware codenames
    """
    async with ClientSession() as session:
        raw = await fetch(session, f'{GITHUB_ORG}/xiaomifirmwareupdater.github.io/'
                                   f'master/data/firmware_codenames.yml')
        codenames = yaml.load(raw, Loader=yaml.FullLoader)
        return codenames


async def load_miui_codenames():
    """
    fetch Xiaomi devices that has miui codenames
    """
    async with ClientSession() as session:
        raw = await fetch(session, f'{GITHUB_ORG}/xiaomifirmwareupdater.github.io/'
                                   f'master/data/miui_codenames.yml')
        codenames = yaml.load(raw, Loader=yaml.FullLoader)
        return codenames


async def load_vendor_codenames():
    """
    fetch Xiaomi devices that has vendor codenames
    """
    async with ClientSession() as session:
        raw = await fetch(session, f'{GITHUB_ORG}/xiaomifirmwareupdater.github.io/'
                                   f'master/data/vendor_codenames.yml')
        codenames = yaml.load(raw, Loader=yaml.FullLoader)
        return codenames


async def load_devices_names():
    """
    fetch Xiaomi devices names
    """
    async with ClientSession() as session:
        raw = await fetch(session, f'{GITHUB_ORG}/xiaomifirmwareupdater.github.io/'
                                   f'master/data/names.yml')
        codenames_names = yaml.load(raw, Loader=yaml.FullLoader)
        names_codenames = {v: k for k, v in codenames_names.items()}
        return codenames_names, names_codenames


async def load_models():
    """
    fetch Xiaomi devices models
    """
    async with ClientSession() as session:
        raw = await fetch(session, f'{GITHUB_ORG}/xiaomi_devices/models/models.json')
        models = json.loads(raw)
        return models


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(load_firmware_codenames(), load_vendor_codenames()))
