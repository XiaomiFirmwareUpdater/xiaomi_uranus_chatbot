""" info messages generator """
from uranus_bot.telegram_bot.tg_bot import LOCALIZE
from uranus_bot.providers.devices_info.info import get_codename


async def models_message(device, models_data, locale):
    """ Generate telegram message of models command """
    message = '**' + LOCALIZE.get_text(locale, "device_models").replace(
        "{models_data[device]['name']}",
        models_data[device]['name']).replace(
        "{device}", device).replace(
        "{models_data[device]['internal_name']}",
        models_data[device]['internal_name']) + ':**\n\n'
    for model, model_name in models_data[device]["models"].items():
        message += f"{model}: {model_name}\n"
    return message


async def models_inline(event, device, models_data, locale):
    """ Generate telegram result of models inline query """
    builder = event.builder
    message = await models_message(device, models_data, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "models_inline").replace("{device}", device),
        text=message)
    return result


async def whatis_message(device, codenames_names, locale):
    """ Generate telegram message of whatis command """
    return LOCALIZE.get_text(
        locale, "whatis_message").replace(
        "{device}", device).replace("{codenames_names[device]}", codenames_names[device])


async def whatis_inline(event, device, codenames_names, locale):
    """ Generate telegram result of whatis inline query """
    builder = event.builder
    message = await whatis_message(device, codenames_names, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "whatis_inline").replace("{device}", device), text=message)
    return result


async def codename_message(device, names_codenames, locale):
    """ Generate telegram message of whatis command """
    message = ""
    info = await get_codename(device, names_codenames)
    if len(info) > 8:
        message = LOCALIZE.get_text(locale, "too_much_codenames").replace("{device}", device)
        return message
    for name, codename in info.items():
        message += LOCALIZE.get_text(locale, "codename_message").replace(
            "{name}", name).replace("{codename}", codename)
    return message


async def codename_inline(event, device, names_codenames, locale):
    """ Generate telegram result of codename inline query """
    builder = event.builder
    message = await codename_message(device, names_codenames, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "codename_inline").replace("{device}", device), text=message)
    return result
