""" Firmware Updates provider """

import yaml
from aiohttp import ClientSession

from uranus_bot import GITHUB_ORG
from uranus_bot.providers.utils.utils import fetch


async def load_firmware_data():
    """
    load latest firmware data form yaml files
    :returns data - a list with merged stable, weekly, current, and EOL data
    """
    async with ClientSession() as session:
        data = yaml.load(await fetch(session,
                                     f'{GITHUB_ORG}/xiaomifirmwareupdater.github.io/master/'
                                     f'data/devices/latest.yml'),
                         Loader=yaml.FullLoader)
        latest = {}
        for item in data:
            codename = item['downloads']['github'].split('/')[4].split('_')[-1]
            version = item['versions']['miui']
            try:
                if latest[codename]:
                    latest.update({codename: latest[codename] + [version]})
            except KeyError:
                latest.update({codename: [version]})
        return latest


async def diff_updates(new, old):
    """ diff firmware updates to get the changes """
    changes = {}
    if not old:
        return changes
    for codename, updates in new.items():
        try:
            _updates = []
            for update in updates:
                if update not in old[codename]:
                    _updates.append(update)
            if _updates:
                changes.update({codename: _updates})
        except KeyError:
            # when a new device is added
            changes.update({codename: updates})
    return changes
