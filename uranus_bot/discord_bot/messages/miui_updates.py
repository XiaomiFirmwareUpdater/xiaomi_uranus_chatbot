""" MIUI Updates generator """
from discord import Embed

from uranus_bot.providers.miui_updates_tracker.miui_updates_tracker import get_miui
from uranus_bot.utils.miui import get_os_type, get_region, get_type
from uranus_bot import XFU_WEBSITE


async def miui_message(device, method, updates, codenames_names):
    """ Generate discord message of recovery/fastboot command """
    data = await get_miui(device, method, updates)
    rom_type = await get_type(str(data))
    embed = Embed(title=f"**Latest {codenames_names[device]}** (`{device}`) "
                        f"**MIUI Official {rom_type} ROMs**")
    for i in data:
        version = i['version']
        android = i['android']
        download = f"https://cdnorg.d.miui.com/{'/'.join(i['link'].split('/')[3:])}"
        embed.add_field(name=f"{i['name']} {version} | {android}",
                        value=f'[Download]({download})', inline=True)
    embed.add_field(name='ROMs Archive', value=f'[Here]({XFU_WEBSITE}/archive/{get_os_type(data)}/{device}/)')
    return embed


async def archive_message(device, codenames_names):
    """ Generate discord message of archive command """
    embed = Embed(title=f'**ROMs archive for {codenames_names[device]}** (`{device}`)')
    embed.add_field(name='HyperOS Archive',
                    value=f'[Download]({XFU_WEBSITE}/archive/hyperos/{device}/)')
    embed.add_field(name='MIUI Archive',
                    value=f'[Download]({XFU_WEBSITE}/archive/miui/{device}/)')
    return embed


async def latest_miui_message(device, updates, codenames_names):
    """ Generate discord message of latest command """
    data = await get_miui(device, "Recovery", updates)
    description = ""
    for i in data:
        version = i['version']
        description += f"{i['name']} {i['branch']}: `{version}`\n"
    embed = Embed(title=f"**Latest OS Versions for {codenames_names[device]}** (`{device}`)",
                  description=description)
    return embed


async def miui_update_message(data, codenames_names):
    """ Generate telegram message of miui update """
    rom_type = await get_type(str(data))
    device = data['codename'].split('_')[0]
    filename = data['link'].split('/')[-1]
    region = await get_region(filename, device, data['version'])
    description = f"**Region:** {region} \n" \
                  f"**Size**: {data['size']}"
    embed = Embed(title=f"**New MIUI {rom_type} Update Available for {codenames_names[device]}** (`{device}`)!",
                  description=description)
    embed.add_field(name=f"{data['version']} | {data['android']}", value=f"[Download]({data['link']})")
    return embed
