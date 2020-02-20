""" MIUI Updates commands handlers """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.miui_updates import miui_message, \
    archive_message, latest_miui_message
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/recovery(?: )?(.+)?'))
@BOT.on(events.NewMessage(pattern='/fastboot(?: )?(.+)?'))
async def miui(event):
    """Send a message when the command /recovery or /fastboot is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        device = DATABASE.get_codename(event.chat_id)
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in list(PROVIDER.miui_codenames):
        await event.reply(await error_message(device, locale))
        return
    updates = PROVIDER.miui_recovery_updates if "recovery" in event.pattern_match.string \
        else PROVIDER.miui_fastboot_updates
    message, buttons = await miui_message(device, updates,
                                          PROVIDER.codenames_names, locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/archive(?: )?(.+)?'))
async def firmware(event):
    """Send a message when the command /archive is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        device = DATABASE.get_codename(event.chat_id)
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in PROVIDER.miui_codenames:
        await event.reply(await error_message(device, locale))
        return
    message, buttons = await archive_message(device, PROVIDER.codenames_names, locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/latest(?: )?(.+)?'))
async def latest(event):
    """Send a message when the command /latest is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        device = DATABASE.get_codename(event.chat_id)
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in list(PROVIDER.miui_codenames):
        await event.reply(await error_message(device, locale))
        return
    message = await latest_miui_message(device, PROVIDER.miui_recovery_updates,
                                        PROVIDER.codenames_names, locale)
    await event.reply(message)
    raise events.StopPropagation
