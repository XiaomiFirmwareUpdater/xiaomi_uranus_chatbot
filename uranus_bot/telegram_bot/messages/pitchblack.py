""" PitchBlack messages generator """
from telethon import Button

from uranus_bot.providers.custom_recovery.pitchblack.pitchblack import get_pitchblack
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def pitchblack_message(device, pitchblack_data, locale):
    """ Generate telegram message of pitchblack command """
    data = await get_pitchblack(device, pitchblack_data)
    message = LOCALIZE.get_text(locale, "pitchblack_message").replace(
        "{device}", device) + ':\n'
    buttons = []
    for file, link in data.items():
        buttons.append([Button.url(f'{file}', url=link)])
    return message, buttons


async def pitchblack_inline(event, device, pitchblack_data, locale):
    """ Generate telegram result of pitchblack inline query """
    builder = event.builder
    message, buttons = await pitchblack_message(device, pitchblack_data, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "pitchblack_inline"),
        text=message, buttons=buttons,
        link_preview=False
    )
    return result
