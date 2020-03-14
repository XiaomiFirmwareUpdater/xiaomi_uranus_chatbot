"""orangefox custom recovery api wrapper"""
import json

from aiohttp import ClientSession

from uranus_bot.providers.utils.utils import fetch


async def get_orangefox(device):
    """
    fetch latest orangefox links for a device
    """
    api_url = "https://api.orangefox.tech"
    host = "https://files.orangefox.tech"
    async with ClientSession() as session:
        devices = json.loads(await fetch(session, f'{api_url}/all_codenames/'))
        if device not in devices:
            return
        downloads = []
        try:
            stable = json.loads(await fetch(session, f'{api_url}/last_stable_release/{device}'))
            downloads.append({f"{stable['file_name']}": f"{host}/" + "/".join(stable['file_path'].split('/')[5:])})
        except json.decoder.JSONDecodeError:
            pass
        try:
            beta = json.loads(await fetch(session, f'{api_url}/last_beta_release/{device}'))
            downloads.append({f"{beta['file_name']}": f"{host}/" + "/".join(beta['file_path'].split('/')[5:])})
        except json.decoder.JSONDecodeError:
            pass
        if downloads:
            info = json.loads(await fetch(session, f'{api_url}/details/{device}'))
            return {'name': info['fullname'], 'maintainer': info['maintainer'], 'downloads': downloads}
