#!/usr/bin/env python3.7
"""Mi Vendor updater"""

from bs4 import BeautifulSoup
from requests import get
from .extras import check_codename, set_branch, set_region
from .mwt import MWT


@MWT(timeout=60*60*6)
def load_data():
    """
    load latest vendor data form json files
    :returns data - a list with merged stable, weekly, current, and EOL data
    """
    stable = get('https://raw.githubusercontent.com/TryHardDood/' +
                 'mi-vendor-updater/master/stable.json').json()
    weekly = get('https://raw.githubusercontent.com/TryHardDood/' +
                 'mi-vendor-updater/master/weekly.json').json()
    return stable, weekly


@MWT(timeout=60*60)
@check_codename
def fetch_vendor(device):
    """
    extract latest vendor links for a device
    :argument device - Xiaomi device codename
    :returns message - telegram message string
    :returns status - Boolean for device status whether found or not
    """
    status = None
    message = ''

    def fetch(data, branch):
        reply = ''
        for i in data:
            for codename, version in i.items():
                version = version.split('_')[1]
                url = 'https://github.com/TryHardDood/mi-vendor-updater/releases/' \
                    f'tag/{codename}-{branch}'
                response = get(url)
                page = BeautifulSoup(response.content, 'html.parser')
                links = [i for i in page.findAll('a') if version in str(i)]
                if not links:
                    continue
                link = BeautifulSoup(str(links), 'html.parser')
                file = link.a['href'].split('/')[-1]
                rom_type = set_branch(version)
                region = set_region(file)
                reply += f"{region} {rom_type}: [{version}](https://github.com{link.a['href']})\n"
        return reply
    stable, weekly = load_data()
    stable = [i for i in stable if device in str(i)]
    if not stable:
        message = f"Can't find info about {device}!"
        status = False
        return message, status
    message += fetch(stable, 'stable')
    weekly = [i for i in weekly if device in str(i)]
    if weekly:
        message += fetch(weekly, 'weekly')
    message += '@MIUIVendorUpdater'
    return message, status
