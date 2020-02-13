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
    """ Get specs of a device by its codename """
    try:
        info = [i for i in specs_data if device == i['codename']][0]
    except IndexError:
        return
    data = {}
    name = info['name']
    url = info['url']
    details = info['specs']
    device_status = details['Launch'][0]['Status']
    network = details['Network'][0]['Technology']
    weight = details['Body'][0]['Weight']
    display = details['Display'][0]['Type'] + '\n' + details['Display'][0]['Size'] + '\n' + \
              details['Display'][0]['Resolution']
    chipset = details['Platform'][0]['Chipset'] + '\n' + details['Platform'][0]['CPU'] + '\n' + \
              details['Platform'][0]['GPU']
    memory = details['Memory'][0]['Internal']
    main_cam = details['Main Camera'][0]
    camera, camera_details = next(iter(main_cam.items()))
    main_cam = f"{camera} {camera_details}"
    front_cam = details['Selfie camera'][0]
    camera, camera_details = next(iter(front_cam.items()))
    front_cam = f"{camera} {camera_details}"
    jack = details['Sound'][0]['3.5mm jack']
    usb = details['Comms'][0]['USB']
    sensors = details['Features'][0]['Sensors']
    battery = details['Battery'][0]['info']
    charging = None
    try:
        charging = details['Battery'][0]['Charging']
    except KeyError:
        pass
    data.update({'name': name, 'url': url, 'status': device_status, 'network': network,
                 'weight': weight, 'display': display, 'chipset': chipset, 'memory': memory,
                 'rear_camera': main_cam, 'front_camera': front_cam, 'jack': jack,
                 'usb': usb, 'sensors': sensors, 'battery': battery})
    if charging:
        data.update({'charging': charging})
    return data
