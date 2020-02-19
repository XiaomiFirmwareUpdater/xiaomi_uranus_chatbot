""" Xiaomi Geeks Telegram Bot help module"""

from telethon import events, Button

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.help import help_main_message, miui_help_message, \
    miscellaneous_help_message, info_help_message, specs_help_message, \
    custom_recovery_help_message, vendor_help_message, firmware_help_message, \
    eu_help_message, subscriptions_help_message, open_in_pm_message
from uranus_bot.telegram_bot.tg_bot import BOT, LOCALIZE


@BOT.on(events.NewMessage(pattern='/help'))
async def show_help(event):
    """Send a message when the command /help is sent."""
    locale = DATABASE.get_locale(event.chat_id)
    if not event.is_private:
        await event.reply(await open_in_pm_message(locale))
    else:
        message, buttons = await help_main_message(locale)
        await event.reply(message, buttons=buttons)
    raise events.StopPropagation


@BOT.on(events.CallbackQuery(data='help'))
async def help_callback(event):
    """help buttons callback for back button"""
    locale = DATABASE.get_locale(event.chat_id)
    message, buttons = await help_main_message(locale)
    await event.edit(message, buttons=buttons)


@BOT.on(events.CallbackQuery(data='miui_help'))
async def miui_help(event):
    """miui help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await miui_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])


@BOT.on(events.CallbackQuery(data='firmware_help'))
async def firmware_help(event):
    """firmware help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await firmware_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])


@BOT.on(events.CallbackQuery(data='vendor_help'))
async def vendor_help(event):
    """vendor help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await vendor_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])


@BOT.on(events.CallbackQuery(data='eu_help'))
async def eu_help(event):
    """eu help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await eu_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])


@BOT.on(events.CallbackQuery(data='custom_recovery_help'))
async def custom_recovery_help(event):
    """custom recovery help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await custom_recovery_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])


@BOT.on(events.CallbackQuery(data='specs_help'))
async def specs_help(event):
    """specs help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await specs_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])


@BOT.on(events.CallbackQuery(data='info_help'))
async def info_help(event):
    """info help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await info_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])


@BOT.on(events.CallbackQuery(data='misc_help'))
async def misc_help(event):
    """misc help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await miscellaneous_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])


@BOT.on(events.CallbackQuery(data='subscriptions_help'))
async def subscriptions_help(event):
    """subscriptions help callback handler"""
    locale = DATABASE.get_locale(event.chat_id)
    await event.edit(await subscriptions_help_message(locale), buttons=[
        [Button.inline(LOCALIZE.get_text(locale, "Back"), data="help")],
    ])
