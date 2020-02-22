""" helps messages generator """
from telethon import Button

from uranus_bot import XFU_WEBSITE
from uranus_bot.telegram_bot.tg_bot import BOT_INFO, LOCALIZE


async def open_in_pm_message(locale):
    """ generate open in pm message """
    message = LOCALIZE.get_text(locale, "open_in_pm")
    buttons = [
        Button.url(LOCALIZE.get_text(locale, "click_here"),
                   f"https://t.me/{BOT_INFO['username']}?start=help")]
    return message, buttons


async def help_main_message(locale):
    """ Generate telegram message of help command """
    message = LOCALIZE.get_text(locale, "help_message").replace(
        "{BOT_INFO['name']}", BOT_INFO['name']).replace(
        "{BOT_INFO['username']}", BOT_INFO['username']
    ).replace("{XFU_WEBSITE}", XFU_WEBSITE)
    buttons = [
        [Button.inline(LOCALIZE.get_text(locale, "Subscriptions"),
                       data="subscriptions_help"),
         Button.inline(LOCALIZE.get_text(locale, "preferred_device"),
                       data="preferred_device_help")],
        [Button.inline(LOCALIZE.get_text(locale, "miui_updates"),
                       data="miui_help"),
         Button.inline(LOCALIZE.get_text(locale, "Firmware"),
                       data="firmware_help")],
        [Button.inline(LOCALIZE.get_text(locale, "Vendor"),
                       data="vendor_help"),
         Button.inline(LOCALIZE.get_text(locale, "xiaomi_eu"),
                       data="eu_help")],
        [Button.inline(LOCALIZE.get_text(locale, "custom_recovery"),
                       data="custom_recovery_help"),
         Button.inline(LOCALIZE.get_text(locale, "devices_specs"),
                       data="specs_help")],
        [Button.inline(LOCALIZE.get_text(locale, "devices_info"),
                       data="info_help"),
         Button.inline(LOCALIZE.get_text(locale, "Miscellaneous"),
                       data="misc_help")]
    ]
    return message, buttons


async def miui_help_message(locale):
    """ Generate telegram message of miui help"""
    example = LOCALIZE.get_text(locale, "Example")
    return f"/recovery `codename`: {LOCALIZE.get_text(locale, 'recovery_help')}\n" \
           f"__{example}:__ `/recovery whyred`\n\n" \
           f"/fastboot `codename`: {LOCALIZE.get_text(locale, 'fastboot_help')}\n" \
           f"__{example}:__ `/fastboot whyred`\n\n" \
           f"/latest `codename`: {LOCALIZE.get_text(locale, 'latest_help')}\n" \
           f"__{example}:__ `/latest sagit`\n\n" \
           f"/archive `codename`: {LOCALIZE.get_text(locale, 'archive_help')}\n" \
           f"__{example}:__ `/archive mido`"


async def firmware_help_message(locale):
    """ Generate telegram message of firmware help"""
    return f"/firmware `codename`: {LOCALIZE.get_text(locale, 'firmware_help')}\n" \
           f"__{LOCALIZE.get_text(locale, 'Example')}:__ `/firmware dipper`"


async def vendor_help_message(locale):
    """ Generate telegram message of vendor help"""
    return f"/vendor `codename`: {LOCALIZE.get_text(locale, 'vendor_help')}\n" \
           f"__{LOCALIZE.get_text(locale, 'Example')}:__ `/vendor dipper`"


async def eu_help_message(locale):
    """ Generate telegram message of eu help"""
    return f"/eu `codename`: {LOCALIZE.get_text(locale, 'eu_help')}\n" \
           f"__{LOCALIZE.get_text(locale, 'Example')}:__ `/eu dipper`"


async def custom_recovery_help_message(locale):
    """ Generate telegram message of custom_recovery help"""
    example = LOCALIZE.get_text(locale, "Example")
    return f"/twrp `codename`: {LOCALIZE.get_text(locale, 'twrp_help')}\n" \
           f"__{example}:__ `/twrp whyred`\n\n" \
           f"/of `codename`: {LOCALIZE.get_text(locale, 'of_help')}\n" \
           f"__{example}:__ `/of whyred`\n\n" \
           f"/pb `codename`: {LOCALIZE.get_text(locale, 'pb_help')}\n" \
           f"__{example}:__ `/pb sagit`"


async def specs_help_message(locale):
    """ Generate telegram message of specs help"""
    return f"/specs `codename`: {LOCALIZE.get_text(locale, 'specs_help')}\n" \
           f"__{LOCALIZE.get_text(locale, 'Example')}:__ `/specs riva`"


async def info_help_message(locale):
    """ Generate telegram message of info help"""
    example = LOCALIZE.get_text(locale, "Example")
    return f"/models `codename`: {LOCALIZE.get_text(locale, 'models_help')}\n" \
           f"__{example}:__ `/models whyred`\n\n" \
           f"/whatis `codename`: {LOCALIZE.get_text(locale, 'whatis_help')}\n" \
           f"__{example}:__ `/whatis whyred`\n\n" \
           f"/codename `codename`: {LOCALIZE.get_text(locale, 'codename_help')}\n" \
           f"__{example}:__ `/codename mi 9t`"


async def miscellaneous_help_message(locale):
    """ Generate telegram message of miscellaneous help"""
    return f"/guides: {LOCALIZE.get_text(locale, 'guides_help')}\n" \
           f"/unlockbl: {LOCALIZE.get_text(locale, 'unlockbl_help')}\n" \
           f"/tools: {LOCALIZE.get_text(locale, 'tools_help')}\n" \
           f"/arb: {LOCALIZE.get_text(locale, 'arb_help')}"


async def subscriptions_help_message(locale):
    """ Generate telegram message of subscriptions help"""
    example = LOCALIZE.get_text(locale, "Example")
    return "/subscribe `firmware`|`miui`|`vendor` `codename`: " \
           f"\n{LOCALIZE.get_text(locale, 'subscribe_help')}\n" \
           f"__{example}:__ `/subscribe firmware whyred`\n\n" \
           f"/unsubscribe `firmware`|`miui`|`vendor` `codename`: " \
           f"\n{LOCALIZE.get_text(locale, 'unsubscribe_help')}\n" \
           f"__{example}:__ `/unsubscribe firmware whyred`\n\n" \
           f"/subscription: {LOCALIZE.get_text(locale, 'subscription_help')}"


async def preferred_device_help_message(locale):
    """ Generate telegram message of preferred device help"""
    example = LOCALIZE.get_text(locale, "Example")
    return f"/set_codename `codename`: {LOCALIZE.get_text(locale, 'preferred_device_help')}\n" \
           f"__{example}:__ `/set_codename whyred`"
