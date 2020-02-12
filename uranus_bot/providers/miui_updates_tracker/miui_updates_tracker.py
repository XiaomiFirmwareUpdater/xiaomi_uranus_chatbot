""" MIUI Updates Tracker provider """

import yaml
from aiohttp import ClientSession

from uranus_bot import GITHUB_ORG
from uranus_bot.providers.utils.utils import fetch


async def load_fastboot_data():
    """
    load latest fasboot ROMs data form MIUI tracker yaml files
    :returns data - a list with merged stable, weekly, current, and EOL data
    """
    async with ClientSession() as session:
        stable_roms = yaml.load(await fetch(session, f'{GITHUB_ORG}/miui-updates-tracker/master/'
                                                     f'stable_fastboot/stable_fastboot.yml'),
                                Loader=yaml.FullLoader)
        weekly_roms = yaml.load(await fetch(session, f'{GITHUB_ORG}/miui-updates-tracker/master/'
                                                     f'weekly_fastboot/weekly_fastboot.yml'),
                                Loader=yaml.FullLoader)
        eol_stable_roms = yaml.load(await fetch(session, f'{GITHUB_ORG}/miui-updates-tracker/master/'
                                                         f'EOL/stable_fastboot/stable_fastboot.yml'),
                                    Loader=yaml.FullLoader)
        eol_weekly_roms = yaml.load(await fetch(session, f'{GITHUB_ORG}/miui-updates-tracker/master/'
                                                         f'EOL/weekly_fastboot/weekly_fastboot.yml'),
                                    Loader=yaml.FullLoader)
        data = [*stable_roms, *weekly_roms, *eol_stable_roms, *eol_weekly_roms]
        return data


async def filter_recovery_weekly(weekly_roms: list) -> list:
    """ Filter weekly recovery roms data to get latest only """
    codenames = [i['codename'] for i in weekly_roms]
    updates = []
    for item in weekly_roms:
        for codename in codenames:
            if item['codename'] == codename and codename not in str(updates):
                updates.append(item)
    return updates


async def load_recovery_data():
    """
    load latest recovery ROMs data form MIUI tracker yaml files
    :returns data - a list with merged stable, weekly, current, and EOL data
    """
    async with ClientSession() as session:
        stable_roms = yaml.load(await fetch(session, f'{GITHUB_ORG}/miui-updates-tracker/master/'
                                                     f'stable_recovery/stable_recovery.yml'),
                                Loader=yaml.FullLoader)
        weekly_roms = yaml.load(await fetch(session, f'{GITHUB_ORG}/xiaomifirmwareupdater.github.io/master/'
                                                     f'data/devices/miui11.yml'),
                                Loader=yaml.FullLoader)
        weekly_roms = await filter_recovery_weekly(weekly_roms)
        eol_stable_roms = yaml.load(await fetch(session, f'{GITHUB_ORG}/miui-updates-tracker/master/'
                                                         f'EOL/stable_recovery/stable_recovery.yml'),
                                    Loader=yaml.FullLoader)
        eol_weekly_roms = yaml.load(await fetch(session, f'{GITHUB_ORG}/miui-updates-tracker/master/'
                                                         f'EOL/weekly_recovery/weekly_recovery.yml'),
                                    Loader=yaml.FullLoader)
        data = [*stable_roms, *weekly_roms, *eol_stable_roms, *eol_weekly_roms]
        return data


async def get_miui(device, updates):
    """ Get miui from for a device """
    return [i for i in updates if device == i['codename'].split('_')[0]]
