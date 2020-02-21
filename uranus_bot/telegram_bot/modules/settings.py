""" Xiaomi Geeks Telegram Bot settings module"""

from telethon import events, Button
from telethon.errors import MessageNotModifiedError

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.miui_updates import subscriptions_message, wrong_codename_message
from uranus_bot.telegram_bot.messages.settings import set_locale_message, \
    settings_main_message, set_locale_pm_message, lang_settings_message, \
    set_codename_message, preferred_device_message
from uranus_bot.telegram_bot.modules.subscriptions import subscription_allowed
from uranus_bot.telegram_bot.tg_bot import BOT, LOCALIZE, PROVIDER


# @BOT.on(events.NewMessage(pattern='/set_lang (.+)'))
# async def set_lang_handler(event):
#     """Send a message when the command /set_lang is sent."""
#     locale = DATABASE.get_locale(event.chat_id)
#     if not await subscription_allowed(event):
#         return
#     lang = event.pattern_match.group(1)
#     if lang in LOCALIZE.locales:
#         if DATABASE.set_locale(event.chat_id, lang):
#             message = await set_locale_message(lang, locale)
#             await event.reply(message)
#     else:
#         await event.reply(await wrong_locale_message(lang, locale))
#     raise events.StopPropagation

@BOT.on(events.CallbackQuery(data='change_language'))
@BOT.on(events.NewMessage(pattern='/set_lang'))
async def set_lang_keyboard(event):
    """Send a message when the command /set_lang is sent"""
    locale = DATABASE.get_locale(event.chat_id)
    if not await subscription_allowed(event):
        return
    message, buttons = await set_locale_pm_message(locale)
    await event.reply(message, buttons=buttons)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern=r'[a-z]{2}(?:-[A-Z]{2})? - \S* \(\S*\)'))
async def set_lang_handler(event):
    """ Set the language based on the user selection"""
    lang = event.message.message.split(' ')[0]
    DATABASE.set_locale(event.chat_id, lang)
    locale = DATABASE.get_locale(event.chat_id)
    message = await set_locale_message(lang, locale)
    await event.reply(message, buttons=Button.clear())
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/set_codename (.+)'))
async def set_codename_handler(event):
    """Send a message when the command /set_codename is sent"""
    locale = DATABASE.get_locale(event.chat_id)
    if not await subscription_allowed(event):
        return
    device = event.pattern_match.group(1)
    if device not in PROVIDER.miui_codenames:
        await event.reply(await wrong_codename_message(locale))
        return
    if DATABASE.set_codename(event.chat_id, device):
        await event.reply(await set_codename_message(device, PROVIDER.codenames_names, locale))
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/settings'))
async def show_settings(event):
    """Send a message when the command /settings is sent."""
    locale = DATABASE.get_locale(event.chat_id)
    if not await subscription_allowed(event):
        return
    message, buttons = await settings_main_message(locale)
    await event.respond(message, buttons=buttons)
    raise events.StopPropagation


@BOT.on(events.CallbackQuery(data='settings'))
async def settings_callback(event):
    """settings buttons callback for back button"""
    locale = DATABASE.get_locale(event.chat_id)
    message, buttons = await settings_main_message(locale)
    await event.edit(message, buttons=buttons)


@BOT.on(events.CallbackQuery(data='subscriptions_settings'))
async def subscriptions_help(event):
    """subscriptions settings callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    subscriptions = DATABASE.get_chat_subscriptions(event.chat_id)
    try:
        await event.edit(await subscriptions_message(subscriptions, locale), buttons=[
            [Button.inline(LOCALIZE.get_text(locale, "Back"), data="settings")],
        ])
    except MessageNotModifiedError:
        pass


@BOT.on(events.CallbackQuery(data='lang_settings'))
async def lang_help(event):
    """language help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    try:
        await event.edit(await lang_settings_message(locale), buttons=[
            [Button.inline(LOCALIZE.get_text(locale, "change_language"),
                           data="change_language")],
            [Button.inline(LOCALIZE.get_text(locale, "Back"), data="settings")]
        ])
    except MessageNotModifiedError:
        pass


@BOT.on(events.CallbackQuery(data='device_settings'))
async def set_codename_help(event):
    """preferred device settings callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    device = DATABASE.get_codename(event.chat_id)
    try:
        await event.edit(await preferred_device_message(device, PROVIDER.codenames_names, locale), buttons=[
            [Button.inline(LOCALIZE.get_text(locale, "change_preferred_device"),
                           data="preferred_device_help")],
            [Button.inline(LOCALIZE.get_text(locale, "Back"), data="settings")]
        ])
    except MessageNotModifiedError:
        pass
