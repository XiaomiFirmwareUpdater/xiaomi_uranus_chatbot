""" OSS messages generator """

from uranus_bot.providers.xiaomi_oss.xiaomi_oss import get_oss
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def oss_message(device, locale):
    """ Generate telegram message of oss command """
    data = await get_oss(device)
    if not data:
        return
    message = ""
    for i in data:
        message += f"**{LOCALIZE.get_text(locale, 'Devices')}:** {i.split('|')[2].strip()}\n" \
                   f"{i.split('|')[3].strip()}\n" \
                   f"**{LOCALIZE.get_text(locale, 'Tag')}:** {i.split('|')[4].strip()}\n" \
                   f"{i.split('|')[5].strip()}\n\n"
    return message


async def oss_inline(event, device, locale):
    """ Generate telegram result of oss inline query """
    builder = event.builder
    message = await oss_message(device, locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "oss_inline").replace("{device}", device),
        text=message)
    return result
