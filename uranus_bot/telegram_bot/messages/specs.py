""" Specs messages generator """

from uranus_bot.providers.specs.specs import get_specs
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def specs_message(device, specs_data, locale):
    """ Generate telegram message of specs command """
    data = await get_specs(device, specs_data)
    if not data:
        return
    message = f"[{data['name']}]({data['url']}) - **{device}**\n" \
              f"**{LOCALIZE.get_text(locale, 'Status')}**: {data['status']}\n" \
              f"**{LOCALIZE.get_text(locale, 'Network')}:** {data['network']}\n" \
              f"**{LOCALIZE.get_text(locale, 'Weight')}**: {data['weight']}\n" \
              f"**{LOCALIZE.get_text(locale, 'Display')}**:\n{data['display']}\n" \
              f"**{LOCALIZE.get_text(locale, 'Chipset')}**:\n{data['chipset']}\n" \
              f"**{LOCALIZE.get_text(locale, 'Memory')}**: {data['memory']}\n" \
              f"**{LOCALIZE.get_text(locale, 'rear_camera')}**: {data['rear_camera']}\n" \
              f"**{LOCALIZE.get_text(locale, 'front_camera')}**: {data['front_camera']}\n" \
              f"**{LOCALIZE.get_text(locale, 'headphone_jack')}**: {data['jack']}\n" \
              f"**{LOCALIZE.get_text(locale, 'USB')}**: {data['usb']}\n" \
              f"**{LOCALIZE.get_text(locale, 'Sensors')}**: {data['sensors']}\n" \
              f"**{LOCALIZE.get_text(locale, 'Battery')}**: {data['battery']}"
    try:
        message += f"\n**{LOCALIZE.get_text(locale, 'Charging')}**: {data['charging']}"
    except KeyError:
        pass
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
        link_preview=True
    )
    return result
