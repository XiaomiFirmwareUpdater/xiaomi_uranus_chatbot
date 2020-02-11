""" Info messages generator """
from discord import Embed


async def models_message(device, models_data):
    """ Generate discord message of twrp command """
    description = ""
    for model, model_name in models_data[device]["models"].items():
        description += f"{model}: {model_name}\n"
    embed = Embed(title=f'**{models_data[device]["name"]} '
                        f'({device} - {models_data[device]["internal_name"]}) Models:**\n\n',
                  description=description)
    return embed


async def whatis_message(device, codenames_names):
    """ Generate discord message of whatis command """
    return Embed(title=f"`{device}` is **{codenames_names[device]}**")


async def codename_message(device, names_codenames):
    """ Generate discord message of codename command """
    info = {}
    for name, codename in names_codenames.items():
        if '/' in name and name.split('/')[1].lower().startswith(device.lower()):
            info.update({name: codename})
        if name.lower().startswith(device.lower()):
            info.update({name: codename})
    if len(info) > 8:
        message = f"{device} is too general! Please be more specific."
        return Embed(title=f"**Search result:**", description=message)
    message = ""
    for name, codename in info.items():
        message += f"**{name}** is `{codename}`\n"
    return Embed(title=f"**Search result:**", description=message)
