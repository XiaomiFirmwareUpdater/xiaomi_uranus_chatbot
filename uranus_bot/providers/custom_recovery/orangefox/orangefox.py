"""orangefox custom recovery downloads scraper"""
import json

from aiohttp import ClientSession

from uranus_bot.providers.utils.utils import fetch


async def load_orangefox_data():
    """
    load orangefox devices info
    """
    async with ClientSession() as session:
        raw = await fetch(session, 'https://files.orangefox.tech/Other/update_v2.json')
        return json.loads(raw)


async def get_orangefox(device, orangefox_data):
    """
    fetch latest orangefox links for a device
    """
    try:
        info = orangefox_data[device]
    except KeyError:
        return
    url = f'https://files.orangefox.tech/OrangeFox'
    downloads = []
    try:
        stable = info['stable_build']
        downloads.append({f"{stable}": f"{url}-Stable/{device}/{stable}"})
    except KeyError:
        pass
    try:
        beta = info['beta_build']
        downloads.append({f"{beta}": f"{url}-Beta/{device}/{beta}"})
    except KeyError:
        pass
    return {'name': info['fullname'], 'maintainer': info['maintainer'], 'downloads': downloads}
