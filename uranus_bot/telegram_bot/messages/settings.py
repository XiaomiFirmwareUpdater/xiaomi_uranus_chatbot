""" settings messages generator """
from telethon import Button

from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def set_locale_message(lang, locale):
    """Generate telegram message for setlang command"""
    return "**" + LOCALIZE.get_text(locale, "set_locale_message").replace("{lang}", lang) + "**"


async def wrong_locale_message(lang, locale):
    """Generate telegram message for setlang command when wrong locale is given"""
    return LOCALIZE.get_text(locale, "wrong_locale_message").replace("{lang}", lang)


async def set_locale_pm_message(locale):
    """Generate telegram message for set_lang command"""
    message = LOCALIZE.get_text(locale, "available_languages")
    buttons = []
    for lang in LOCALIZE.locales:
        buttons.append([
            Button.text(f"{lang} - {LOCALIZE.all_locales[lang]['name']} "
                        f"({LOCALIZE.all_locales[lang]['nativeName']})",
                        resize=True)])
    return message, buttons


async def set_codename_message(device, codenames_names, locale):
    """Generate telegram message for set_codename command"""
    return "**" + LOCALIZE.get_text(locale, "set_device_message").replace(
        "{device}", device).replace("{codenames_names[device]}", codenames_names[device]) + "**"


async def settings_main_message(locale):
    """ Generate telegram message of settings command """
    message = "**" + LOCALIZE.get_text(locale, "settings_message") + "**"
    buttons = [
        [Button.inline(LOCALIZE.get_text(locale, "Subscriptions"),
                       data="subscriptions_settings")],
        [Button.inline(LOCALIZE.get_text(locale, "bot_lang"),
                       data="lang_settings")],
        [Button.inline(LOCALIZE.get_text(locale, "preferred_device"),
                       data="device_settings")]
    ]
    return message, buttons


async def lang_settings_message(locale):
    """ Generate telegram message of language settings"""
    return f"**{LOCALIZE.get_text(locale, 'bot_lang')}**: {locale}"


async def preferred_device_message(device, codenames_names, locale):
    """ Generate preferred device message"""
    if device:
        message = f"**" + LOCALIZE.get_text(locale, "your_preferred_device") + ":**\n" +\
            f"{codenames_names[device]} (`{device}`)"
    else:
        message = f"**{LOCALIZE.get_text(locale, 'no_subscriptions')}**"
    return message
