""" MIUI Updates generator """
from discord import Embed

from uranus_bot.providers.miui_updates_tracker.miui_updates_tracker import get_miui
from uranus_bot.utils.miui import get_region, get_type, get_branch
from uranus_bot import XFU_WEBSITE


async def miui_message(device, updates, codenames_names):
    """ Generate discord message of recovery/fastboot command """
    data = await get_miui(device, updates)
    rom_type = await get_type(str(data))
    embed = Embed(title=f"**Latest {codenames_names[device]}** (`{device}`) "
                        f"**MIUI Official {rom_type} ROMs**")
    for i in data:
        version = i['version']
        android = i['android']
        download = i['download']
        region = await get_region(download.split('/')[-1], i['codename'], version)
        embed.add_field(name=f"{region} {version} | {android}",
                        value=f'[Download]({download})', inline=True)
    embed.add_field(name='ROMs Archive', value=f'[Here]({XFU_WEBSITE}/archive/miui/{device}/)')
    return embed


async def archive_message(device, codenames_names):
    """ Generate discord message of archive command """
    embed = Embed(title=f'**MIUI ROMs archive for {codenames_names[device]}** (`{device}`)')
    embed.add_field(name='MIUI Archive',
                    value=f'[Download]({XFU_WEBSITE}/archive/miui/{device}/)')
    return embed


async def latest_miui_message(device, updates, codenames_names):
    """ Generate discord message of latest command """
    data = await get_miui(device, updates)
    description = ""
    for i in data:
        version = i['version']
        download = i['download']
        filename = download.split('/')[-1]
        branch = await get_branch(version)
        region = await get_region(filename, i['codename'], version)
        description += f"{region} {branch}: `{version}`\n"
    embed = Embed(title=f"**Latest MIUI Versions for {codenames_names[device]}** (`{device}`)",
                  description=description)
    return embed
