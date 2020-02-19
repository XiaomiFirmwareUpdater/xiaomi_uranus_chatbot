""" TWRP messages generator """
from telethon import Button

from uranus_bot.providers.custom_recovery.twrp.twrp import get_twrp
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def twrp_message(device, twrp_data, locale):
    """ Generate telegram message of twrp command """
    data = await get_twrp(device, twrp_data)
    message = LOCALIZE.get_text(locale, "twrp_message").replace(
        "{data['name']}", data['name']).replace(
        "{data['date']}", data['date']
    )
    buttons = [
        [Button.url(f'{data["dl_file"]} - {data["size"]}', url=data["dl_link"])]
    ]
    return message, buttons


async def twrp_inline(event, device, twrp_data, locale):
    """ Generate telegram result of twrp inline query """
    builder = event.builder
    message, buttons = await twrp_message(device, twrp_data, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "twrp_inline"),
        text=message,
        buttons=buttons,
        link_preview=False
    )
    return result
