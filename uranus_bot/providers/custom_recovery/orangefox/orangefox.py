"""orangefox custom recovery api wrapper"""
import json

from aiohttp import ClientSession

from uranus_bot.providers.utils.utils import fetch


async def get_orangefox(device):
    """
    fetch latest orangefox links for a device
    """
    api_url = "https://api.orangefox.download/v2"
    host = "https://files.orangefox.tech"
    async with ClientSession() as session:
        devices = None
        try:
            devices = json.loads(await fetch(session, f'{api_url}/device'))
        except json.decoder.JSONDecodeError:
            device = None
        if device not in [i['codename'] for i in devices]:
            return
        downloads = []
        try:
            stable = json.loads(await fetch(session, f'{api_url}/device/{device}/releases/stable/last'))
            downloads.append({f"{stable['file_name']}": stable['url']})
        except json.decoder.JSONDecodeError:
            pass
        try:
            beta = json.loads(await fetch(session, f'{api_url}/device/{device}/releases/beta/last'))
            downloads.append({f"{beta['file_name']}": beta['url']})
        except json.decoder.JSONDecodeError:
            pass
        if downloads:
            info = json.loads(await fetch(session, f'{api_url}/device/{device}'))
            return {'name': info['fullname'], 'maintainer': info['maintainer']['name'], 'downloads': downloads}
