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
    """Generate telegram message for setlang command"""
    message = LOCALIZE.get_text(locale, "available_languages")
    buttons = []
    for lang in LOCALIZE.locales:
        buttons.append([
            Button.text(f"{lang} - {LOCALIZE.all_locales[lang]['name']} "
                        f"({LOCALIZE.all_locales[lang]['nativeName']})",
                        resize=True)])
    return message, buttons


async def settings_main_message(locale):
    """ Generate telegram message of settings command """
    message = "**" + LOCALIZE.get_text(locale, "settings_message") + "**"
    buttons = [
        [Button.inline(LOCALIZE.get_text(locale, "Subscriptions"),
                       data="subscriptions_settings")],
        [Button.inline(LOCALIZE.get_text(locale, "bot_lang"),
                       data="lang_settings")]
    ]
    return message, buttons


async def subscriptions_settings_message(locale):
    """ Generate telegram message of subscriptions settings"""
    example = LOCALIZE.get_text(locale, "Example")
    return f"/recovery `codename`: {LOCALIZE.get_text(locale, 'recovery_help')}\n" \
           f"__{example}:__ `/recovery whyred`\n\n" \
           f"/fastboot `codename`: {LOCALIZE.get_text(locale, 'fastboot_help')}\n" \
           f"__{example}:__ `/fastboot whyred`\n\n" \
           f"/latest `codename`: {LOCALIZE.get_text(locale, 'latest_help')}\n" \
           f"__{example}:__ `/latest sagit`\n\n" \
           f"/archive `codename`: {LOCALIZE.get_text(locale, 'archive_help')}\n" \
           f"__{example}:__ `/archive mido`"


async def lang_settings_message(locale):
    """ Generate telegram message of language settings"""
    return f"**{LOCALIZE.get_text(locale, 'bot_lang')}**: {locale}"
