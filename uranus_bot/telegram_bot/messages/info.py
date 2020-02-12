""" info messages generator """
from uranus_bot.providers.devices_info.info import get_codename


async def models_message(device, models_data):
    """ Generate telegram message of models command """
    message = f'**{models_data[device]["name"]} ' \
              f'({device} - {models_data[device]["internal_name"]}) Models:**\n\n'
    for model, model_name in models_data[device]["models"].items():
        message += f"{model}: {model_name}\n"
    return message


async def models_inline(event, device, models_data):
    """ Generate telegram result of models inline query """
    builder = event.builder
    message = await models_message(device, models_data)
    result = builder.article(
        f'Search {device} device models', text=message)
    return result


async def whatis_message(device, codenames_names):
    """ Generate telegram message of whatis command """
    return f"`{device}` is **{codenames_names[device]}**"


async def whatis_inline(event, device, codenames_names):
    """ Generate telegram result of whatis inline query """
    builder = event.builder
    message = await whatis_message(device, codenames_names)
    result = builder.article(
        f'Search {device} device name', text=message)
    return result


async def codename_message(device, names_codenames):
    """ Generate telegram message of whatis command """
    message = ""
    info = await get_codename(device, names_codenames)
    if len(info) > 8:
        message = f"{device} is too general! Please be more specific."
        return message
    for name, codename in info.items():
        message += f"**{name}** is `{codename}`\n"
    return message


async def codename_inline(event, device, names_codenames):
    """ Generate telegram result of whatis inline query """
    builder = event.builder
    message = await codename_message(device, names_codenames)
    result = builder.article(
        f'Search {device} device codename', text=message)
    return result
