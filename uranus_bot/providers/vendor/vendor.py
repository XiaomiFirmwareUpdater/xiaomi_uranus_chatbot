""" Vendor Updates provider """

import yaml
from aiohttp import ClientSession

from uranus_bot import GITHUB_ORG
from uranus_bot.providers.utils.utils import fetch


async def load_vendor_data():
    """
    load latest vendor data form yaml files
    :returns data - a list with merged stable, weekly, current, and EOL data
    """
    async with ClientSession() as session:
        data = yaml.load(await fetch(
            session, f'{GITHUB_ORG}/xiaomifirmwareupdater.github.io/master/'
                     f'data/vendor/latest.yml'),
                         Loader=yaml.FullLoader)
        latest = {}
        for item in data:
            codename = item['downloads']['github'].split('/')[7].split('_')[0].split('-')[0]
            version = item['versions']['miui']
            try:
                if latest[codename]:
                    latest.update({codename: latest[codename] + [version]})
            except KeyError:
                latest.update({codename: [version]})
        return latest
