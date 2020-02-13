""" OSS messages generator """

from uranus_bot.providers.xiaomi_oss.xiaomi_oss import get_oss


async def oss_message(device):
    """ Generate telegram message of oss command """
    data = await get_oss(device)
    if not data:
        return
    message = ""
    for i in data:
        message += f"**Devices:** {i.split('|')[2].strip()}\n" \
                   f"{i.split('|')[3].strip()}\n" \
                   f"**Tag:** {i.split('|')[4].strip()}\n" \
                   f"{i.split('|')[5].strip()}\n\n"
    return message


async def oss_inline(event, device):
    """ Generate telegram result of oss inline query """
    builder = event.builder
    message = await oss_message(device)
    result = builder.article(
        f'Search {device} OSS kernel',
        text=message)
    return result
