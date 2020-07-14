""" MIUI Updates Tracker provider """
import logging

import yaml
from aiohttp import ClientSession

from uranus_bot import GITHUB_ORG
from uranus_bot.providers.utils.utils import fetch

DIFF_LOGGER = logging.getLogger(__name__)


# async def filter_recovery_weekly(weekly_roms: list) -> list:
#     """ Filter weekly recovery roms data to get latest only """
#     codenames = [i['codename'] for i in weekly_roms]
#     updates = []
#     for item in weekly_roms:
#         for codename in codenames:
#             if item['codename'] == codename and codename not in str(updates):
#                 updates.append(item)
#     return updates


async def load_roms_data():
    """
    load recovery ROMs data form MIUI tracker yaml file
    :returns data - a list with latest updates
    """
    async with ClientSession() as session:
        roms = yaml.load(await fetch(
            session, f'{GITHUB_ORG}/miui-updates-tracker/V3/data/latest.yml'),
                         Loader=yaml.FullLoader)
        return roms


async def get_miui(device, method, updates):
    """ Get miui from for a device """
    return [i for i in updates if i['codename'].split('_')[0] == device and i['method'] == method]


async def diff_miui_updates(new, old):
    """ diff miui updates to get the changes """
    changes = {}
    if not old:
        return changes
    for item in new:
        for old_item in old:
            if old_item['codename'] == item['codename'] and item['version'] != old_item['version']:
                is_new = None
                if "V" in item['version'] and "V" in old_item['version']:  # miui stable
                    new_version_array = item['version'].split('.')
                    old_version_array = old_item['version'].split('.')
                    if new_version_array[-1][0] > old_version_array[-1][0]:
                        is_new = True  # new android version
                    elif int(new_version_array[0][1:]) > int(old_version_array[0][1:]):
                        is_new = True  # new miui version
                    elif int(new_version_array[1]) > int(old_version_array[1]):
                        is_new = True  # new miui sub-version
                    elif int(new_version_array[2]) > int(old_version_array[2]):
                        is_new = True  # new miui minor version
                elif "V" not in item['version'] and "V" not in old_item['version'] \
                        and item['version'][0].isdigit() and old_item['version'][0].isdigit():  # miui weekly
                    new_version_array = item['version'].split('.')
                    old_version_array = old_item['version'].split('.')
                    if int(new_version_array[0]) > int(old_version_array[0]):
                        is_new = True
                    elif int(new_version_array[1]) > int(old_version_array[1]):
                        is_new = True
                    elif int(new_version_array[2]) > int(old_version_array[2]):
                        is_new = True
                if is_new:
                    codename = item['codename'].split('_')[0]
                    try:
                        if changes[codename]:
                            changes.update({codename: changes[codename] + [item]})
                    except KeyError:
                        # when a new device is added
                        changes.update({codename: [item]})
    if changes:
        DIFF_LOGGER.info(f"MIUI changes:\n{str(changes)}")
    return changes
