""" helps messages generator """
from telethon import Button

from uranus_bot import XFU_WEBSITE
from uranus_bot.telegram_bot.tg_bot import BOT_INFO


async def help_main_message():
    """ Generate telegram message of help command """
    message = f"**How to use {BOT_INFO['name']}**\n\n" \
              f"@{BOT_INFO['username']} is an all-in-one bot for Xiaomi users!\n" \
              f"It can get you latest Official ROMs, Firmware updates links, and many more things!\n" \
              f"The full usage guide is available [Here]({XFU_WEBSITE}/projects/uranus-chatbot/#usage)" \
              f"Here are all commands available:\n\n" \
              f"/start: Check if bot is running\n" \
              f"/help: Show this help message"
    buttons = [
        [Button.inline("MIUI Updates", data="miui_help"),
         Button.inline("Firmware", data="firmware_help")],
        [Button.inline("Vendor", data="vendor_help"),
         Button.inline("Xiaomi.eu", data="eu_help")],
        [Button.inline("Custom Recovery", data="custom_recovery_help"),
         Button.inline("Devices specs", data="specs_help")],
        [Button.inline("Devices Information", data="info_help"),
         Button.inline("Miscellaneous", data="misc_help")]
    ]
    return message, buttons


async def miui_help_message():
    """ Generate telegram message of miui help"""
    return "/recovery `codename`: Gets latest recovery ROMs info and links\n" \
           "__Example:__ `/recovery whyred`\n" \
           "/fastboot `codename`: Gets latest fastboot ROMs info and links\n" \
           "__Example:__ `/fastboot whyred`\n" \
           "/latest `codename`: Gets latest MIUI versions info\n" \
           "__Example:__ `/latest sagit`\n" \
           "/archive `codename`: Send all official available MIUI ROMs for device archive link\n" \
           "__Example:__ `/archive mido`"


async def firmware_help_message():
    """ Generate telegram message of firmware help"""
    return "/firmware `codename`: Gets available firmware for a device\n" \
           "__Example:__ `/firmware dipper`"


async def vendor_help_message():
    """ Generate telegram message of vendor help"""
    return "/vendor `codename`: Gets available firmware+vendor for a device\n" \
           "__Example:__ `/vendor dipper`"


async def eu_help_message():
    """ Generate telegram message of eu help"""
    return "/eu `codename`: Gets latest Xiaomi EU ROMs downloads for device\n" \
           "__Example:__ `/eu dipper`"


async def custom_recovery_help_message():
    """ Generate telegram message of custom_recovery help"""
    return "/twrp `codename`: Gets latest TWRP download link for device\n" \
           "__Example:__ `/twrp whyred`\n" \
           "/of `codename`: Gets latest PitchBlack recovery download link for device\n" \
           "__Example:__ `/of whyred`\n" \
           "/pb `codename`: Gets latest OrangeFox recovery download link for device\n" \
           "__Example:__ `/pb sagit`"


async def specs_help_message():
    """ Generate telegram message of specs help"""
    return "/specs `codename`: Gets device specs from GSMArena\n" \
           "__Example:__ `/specs riva`"


async def info_help_message():
    """ Generate telegram message of miui help"""
    return "/models `codename`: Gets all available models of a device\n" \
           "__Example:__ `/models whyred`\n" \
           "/whatis `codename`: Tells you which device's codename is this\n" \
           "__Example:__ `/whatis whyred`\n" \
           "/codename `codename`: Tells you what is the codename of this device\n" \
           "__Example:__ `/codename sagit`"


async def miscellaneous_help_message():
    """ Generate telegram message of miui help"""
    return "/guides: Various useful guides for every Xiaomi user\n" \
           "/unlockbl: Unlocking bootloader help and tools\n" \
           "/tools: Various useful tools for every Xiaomi user\n" \
           "/arb: Anti-Rollback Protection information" \
