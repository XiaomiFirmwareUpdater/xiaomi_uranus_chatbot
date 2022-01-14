""" MIUI Updates Tracker provider """
import logging
from datetime import datetime
from itertools import groupby

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
            session, f'{GITHUB_ORG}/miui-updates-tracker/master/data/latest.yml'),
                         Loader=yaml.FullLoader)
        latest = {}
        for item in roms:
            codename = item['codename'].split('_')[0]
            try:
                if latest[codename]:
                    latest.update({codename: latest[codename] + [item]})
            except KeyError:
                latest.update({codename: [item]})
        return latest


async def get_miui(device, method, updates):
    """ Get miui from for a device """
    device_updates = [i for i in updates.get(device) if i and i['method'] == method]
    grouped_by_name = [list(item) for _, item in
                       groupby(sorted(device_updates, key=lambda x: x['name']), lambda x: x['name'])]
    final_updates = []
    for group in grouped_by_name:
        weekly = list(filter(lambda x: x['branch'] == "Weekly", group))
        stable = list(filter(lambda x: x['branch'] == "Stable", group))
        stable_beta = list(filter(lambda x: x['branch'] == "Stable Beta", group))
        public_beta = list(filter(lambda x: x['branch'] == "Public Beta", group))
        if stable_beta and stable:
            if stable_beta[0]['date'] and stable[0]['date']:
                if stable_beta[0]['date'] >= stable[0]['date']:
                    final_updates.append(stable_beta[0])
            else:
                final_updates.append(stable_beta[0])
            final_updates.append(stable[0])
        else:
            if stable:
                final_updates.append(stable[0])
            if stable_beta:
                final_updates.append(stable_beta[0])
        if public_beta:
            final_updates.append(public_beta[0])
        if weekly:
            final_updates.append(weekly[0])
    return final_updates


# async def diff_miui_updates(new, old):
#     """ diff miui updates to get the changes """
#     changes = {}
#     if not old:
#         return changes
#     for item in new:
#         for old_item in old:
#             if old_item['codename'] == item['codename'] and item['version'] != old_item['version']:
#                 is_new = None
#                 if "V" in item['version'] and "V" in old_item['version']:  # miui stable
#                     new_version_array = item['version'].split('.')
#                     old_version_array = old_item['version'].split('.')
#                     if new_version_array[-1][0] > old_version_array[-1][0]:
#                         is_new = True  # new android version
#                     elif int(new_version_array[0][1:]) > int(old_version_array[0][1:]):
#                         is_new = True  # new miui version
#                     elif int(new_version_array[1]) > int(old_version_array[1]):
#                         is_new = True  # new miui sub-version
#                     elif int(new_version_array[2]) > int(old_version_array[2]):
#                         is_new = True  # new miui minor version
#                 elif "V" not in item['version'] and "V" not in old_item['version'] \
#                         and item['version'][0].isdigit() and old_item['version'][0].isdigit():  # miui weekly
#                     new_version_array = item['version'].split('.')
#                     old_version_array = old_item['version'].split('.')
#                     if int(new_version_array[0]) > int(old_version_array[0]):
#                         is_new = True
#                     elif int(new_version_array[1]) > int(old_version_array[1]):
#                         is_new = True
#                     elif int(new_version_array[2]) > int(old_version_array[2]):
#                         is_new = True
#                 if is_new:
#                     codename = item['codename'].split('_')[0]
#                     try:
#                         if changes[codename]:
#                             changes.update({codename: changes[codename] + [item]})
#                     except KeyError:
#                         # when a new device is added
#                         changes.update({codename: [item]})
#     if changes:
#         DIFF_LOGGER.info(f"MIUI changes:\n{str(changes)}")
#     return changes


def is_new_update(update, last_update):
    to_post = False
    if not last_update['date']:
        to_post = True
    else:
        if update['version'] != last_update['version'] \
                and update['date'] > \
                datetime.strptime(last_update['date'], '%Y-%m-%d').date():
            to_post = True
    return to_post
