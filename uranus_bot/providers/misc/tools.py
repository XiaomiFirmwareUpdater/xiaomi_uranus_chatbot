"""Tools info provider"""

from uranus_bot.providers.misc import WIKI


async def get_tools():
    """various tools for Xiaomi devices"""
    url = f'{WIKI}/Tools_for_Xiaomi_devices.html'
    return [{
        "Mi Flash Tool": f"{url}#miflash-by-xiaomi",
        "MiFlash Pro": f"{url}#miflash-pro-by-xiaomi",
        "Mi Unlock Tool": f"{url}#miunlock-by-xiaomi",
        "XiaomiTool": f"{url}#xiaomitool-v2-by-francesco-tescari",
        "XiaomiADB": f"{url}#xiaomiadb-by-francesco-tescari",
        "Unofficial MiUnlock": f"{url}#miunlocktool-by-francesco-tescari",
        "Xiaomi ADB/Fastboot Tools": f"{url}#xiaomi-adbfastboot-tools-by-saki_eu",
        "More Tools": f"{url}"
    }]
