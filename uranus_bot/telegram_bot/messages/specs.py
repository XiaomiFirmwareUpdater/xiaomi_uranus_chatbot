""" Specs messages generator """

from uranus_bot.providers.specs.specs import get_specs
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def specs_message(device, specs_data, locale):
    """ Generate telegram message of specs command """
    datas = await get_specs(device, specs_data)
    specs = []
    for data in datas:
        spec = f"<a href=\"{data['url']}\">{data['name']}</a> - <b>{device}</b>\n" \
                f"<b>{LOCALIZE.get_text(locale, 'Status')}</b>: {data['status']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'Network')}:</b> {data['network']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'Weight')}</b>: {data['weight']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'Display')}</b>:\n{data['display']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'Chipset')}</b>:\n{data['chipset']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'Memory')}</b>: {data['memory']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'rear_camera')}</b>: {data['rear_camera']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'front_camera')}</b>: {data['front_camera']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'headphone_jack')}</b>: {data['jack']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'USB')}</b>: {data['usb']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'Sensors')}</b>: {data['sensors']}\n" \
                f"<b>{LOCALIZE.get_text(locale, 'Battery')}</b>: {data['battery']}"
        try:
            spec += f"\n<b>{LOCALIZE.get_text(locale, 'Charging')}</b>: {data['charging']}"
        except KeyError:
            pass
        specs.append(spec)
    if len(specs) == 0:
        return
    message = '\n\n'.join(specs)
    return message


async def specs_inline(event, device, specs_data, locale):
    """ Generate telegram result of specs inline query """
    builder = event.builder
    message = await specs_message(device, specs_data, locale)
    if not message:
        return
    result = builder.article(
        LOCALIZE.get_text(locale, "specs_inline").replace("{device}", device),
        text=message,
        link_preview=True,
        parse_mode="htm"
    )
    return result
