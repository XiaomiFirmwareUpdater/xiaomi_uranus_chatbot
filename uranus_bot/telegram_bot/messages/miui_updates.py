""" MIUI Updates messages generator """
from telethon import Button

from uranus_bot.providers.miui_updates_tracker.miui_updates_tracker import get_miui
from uranus_bot.utils.miui import get_region, get_type, get_branch
from uranus_bot import XFU_WEBSITE


async def miui_message(device, updates, codenames_names):
    """ Generate telegram message of recovery/fasboot command """
    data = await get_miui(device, updates)
    rom_type = await get_type(str(data))
    message = f"**Latest {codenames_names[device]}** (`{device}`) **MIUI Official {rom_type} ROMs**"
    buttons = []
    for i in data:
        version = i['version']
        android = i['android']
        download = i['download']
        region = await get_region(download.split('/')[-1], i['codename'], version)
        buttons.append([Button.url(f"{region} {version} | {android}", url=download)])
    buttons.append([Button.url(f'ROMs Archive', url=f"{XFU_WEBSITE}/archive/miui/{device}/"),
                    Button.url(f'MIUIUpdatesTracker', url="https://t.me/MIUIUpdatesTracker")])
    return message, buttons


async def miui_inline(event, device, updates, codenames_names):
    """ Generate telegram result of recovery/fasboot inline query """
    builder = event.builder
    message, buttons = await miui_message(device, updates, codenames_names)
    result = builder.article(
        f'Search {codenames_names[device]} ({device}) Official ROMs Downloads',
        text=message, buttons=buttons,
        link_preview=False
    )
    return result


async def archive_message(device, codenames_names):
    """ Generate telegram message of archive command """
    message = f'**MIUI ROMs archive for {codenames_names[device]}** (`{device}`)\n'
    buttons = [
        [Button.url("ROMs Archive", f"{XFU_WEBSITE}/archive/miui/{device}/"),
         Button.url("MIUIUpdatesTracker", "https://t.me/MIUIUpdatesTracker")]
    ]
    return message, buttons


async def archive_inline(event, device, codenames_names):
    """ Generate telegram result of archive inline query """
    builder = event.builder
    message, buttons = await archive_message(device, codenames_names)
    result = builder.article(
        f'Search {codenames_names[device]} ({device}) Official ROMs archive', text=message,
        buttons=buttons, link_preview=False
    )
    return result


async def latest_miui_message(device, updates, codenames_names):
    """ Generate telegram message for latest command """
    data = await get_miui(device, updates)
    message = f"**Latest MIUI Versions for {codenames_names[device]}** (`{device}`):\n"
    for i in data:
        version = i['version']
        download = i['download']
        filename = download.split('/')[-1]
        branch = await get_branch(version)
        region = await get_region(filename, i['codename'], version)
        message += f"{region} {branch}: `{version}`\n"
    return message


async def latest_miui_inline(event, device, updates, codenames_names):
    """ Generate telegram result of latest inline query """
    builder = event.builder
    message = await latest_miui_message(device, updates, codenames_names)
    result = builder.article(
        f'Search {codenames_names[device]} ({device}) latest MIUI versions', text=message)
    return result
