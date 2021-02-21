"""orangefox custom recovery"""
from typing import Optional

from orangefoxapi import ReleaseType
from orangefoxapi.models import Devices, Releases, Release, Device
from orangefoxapi.asynchronous import OrangeFoxAsyncAPI


async def get_orangefox(device):
    """
    fetch latest orangefox links for a device
    """
    api = OrangeFoxAsyncAPI()
    devices: Devices = await api.devices(oem_name='Xiaomi')
    if device not in [i.codename for i in devices.data]:
        return
    device: Optional[Device] = await api.device(codename=device)
    if not device:
        return
    downloads = []
    for releases_type in [ReleaseType.stable, ReleaseType.beta]:
        releases: Releases = await api.releases(device_id=device.id, limit=1, type=releases_type)
        if releases.data:
            release: Optional[Release] = await api.release(id=releases.data[0].id)
            if release:
                downloads.append({f"{release.filename}": release.url})
    await api.close()
    if downloads:
        return {'name': device.full_name, 'maintainer': device.maintainer.name, 'downloads': downloads}
