""" Main messages generator """
from discord import Embed, Colour
from uranus_bot import XFU_WEBSITE, HELP_URL


async def start_message():
    """ Generate discord message  of start command """
    message = f"Hey! I'm Uranus, an all-in-one bot for Xiaomi users!\n" \
              "I can get you latest Official ROMs, Firmware updates links," \
              " and many more things!\n\nCheck how to use me by using !help command.\n\n"
    embed = Embed(title="Welcome!", description=message, color=Colour.orange())
    embed.add_field(name="XiaomiFirmwareUpdater website", value=f"[Here]({XFU_WEBSITE})")
    embed.add_field(name="Read help", value=f"[Here]({HELP_URL})")
    return embed
