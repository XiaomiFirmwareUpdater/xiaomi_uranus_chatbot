""" Devices specifications provider """
import json

from aiohttp import ClientSession

from uranus_bot import GITHUB_ORG
from uranus_bot.providers.utils.utils import fetch


async def load_specs_data():
    """
    fetch Xiaomi devices models
    """
    async with ClientSession() as session:
        raw = await fetch(session, f'{GITHUB_ORG}/xiaomi_devices/gsmarena/devices.json')
        specs = json.loads(raw)
        return specs


async def get_specs(device, specs_data):
    """ Get specs of devices by their codename """
    #pylint: disable=too-many-locals
    try:
        infos = [i for i in specs_data if device in i['codenames']]
    except IndexError:
        return
    datas = []
    for info in infos:
        data = {}
        name = info['name']
        url = info['url']
        details = info['specs']
        device_status = details['Launch']['Status']
        network = details['Network']['Technology']
        weight = details['Body']['Weight']
        display = details['Display']['Type'] + '\n' + details['Display']['Size'] + '\n' + \
                details['Display']['Resolution']
        chipset = details['Platform']['Chipset'] + '\n' + details['Platform']['CPU'] + '\n' + \
                details['Platform']['GPU']
        memory = details['Memory']['Internal']
        main_cam = details['Main Camera']
        camera, camera_details = next(iter(main_cam.items()))
        main_cam = f"{camera} {camera_details}"
        front_cam = details['Selfie camera']
        camera, camera_details = next(iter(front_cam.items()))
        front_cam = f"{camera} {camera_details}"
        jack = details['Sound']['3.5mm jack']
        usb = details['Comms']['USB']
        sensors = details['Features']['Sensors']
        battery = details['Battery']['Type']
        charging = None
        try:
            charging = details['Battery']['Charging']
        except KeyError:
            pass
        data.update({'name': name, 'url': url, 'status': device_status, 'network': network,
                    'weight': weight, 'display': display, 'chipset': chipset, 'memory': memory,
                    'rear_camera': main_cam, 'front_camera': front_cam, 'jack': jack,
                    'usb': usb, 'sensors': sensors, 'battery': battery})
        if charging:
            data.update({'charging': charging})
        datas.append(data)
    return datas
