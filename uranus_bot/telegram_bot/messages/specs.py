""" Specs messages generator """

from uranus_bot.providers.specs.specs import get_specs


async def specs_message(device, specs_data):
    """ Generate telegram message of specs command """
    data = await get_specs(device, specs_data)
    if not data:
        return
    message = f"[{data['name']}]({data['url']}) - **{device}**\n" \
              f"**Status**: {data['status']}\n" \
              f"**Network:** {data['network']}\n" \
              f"**Weight**: {data['weight']}\n" \
              f"**Display**:\n{data['display']}\n" \
              f"**Chipset**:\n{data['chipset']}\n" \
              f"**Memory**: {data['memory']}\n" \
              f"**Rear Camera**: {data['rear_camera']}\n" \
              f"**Front Camera**: {data['front_camera']}\n" \
              f"**3.5mm jack**: {data['jack']}\n" \
              f"**USB**: {data['usb']}\n" \
              f"**Sensors**: {data['sensors']}\n" \
              f"**Battery**: {data['battery']}"
    try:
        message += f"\n**Charging**: {data['charging']}"
    except KeyError:
        pass
    return message


async def specs_inline(event, device, specs_data):
    """ Generate telegram result  of specs inline query """
    builder = event.builder
    message = await specs_message(device, specs_data)
    result = builder.article(
        f'Search {device} Specifications',
        text=message,
        link_preview=True
    )
    return result
