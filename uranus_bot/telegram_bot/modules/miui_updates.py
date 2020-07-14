""" MIUI Updates commands handlers """
from telethon import events
from telethon.errors import ChatWriteForbiddenError

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.miui_updates import miui_message, \
    archive_message, latest_miui_message
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern=r'/recovery(?: )?(\w+)?'))
@BOT.on(events.NewMessage(pattern=r'/fastboot(?: )?(\w+)?'))
async def miui(event):
    """Send a message when the command /recovery or /fastboot is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        if event.message.message.endswith('/recovery') \
                or event.message.message.endswith('/fastboot'):
            device = DATABASE.get_codename(event.chat_id)
        else:
            return
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in list(PROVIDER.miui_codenames):
        await event.reply(await error_message(device, locale))
        return
    method = "Recovery" if "recovery" in event.pattern_match.string else "Fastboot"
    message, buttons = await miui_message(device, method, PROVIDER.miui_updates,
                                          PROVIDER.codenames_names, locale)
    try:
        await event.reply(message, buttons=buttons, link_preview=False)
    except ChatWriteForbiddenError:
        pass
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern=r'/archive(?: )?(\w+)?'))
async def firmware(event):
    """Send a message when the command /archive is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        if event.message.message.endswith('/archive'):
            device = DATABASE.get_codename(event.chat_id)
        else:
            return
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in PROVIDER.miui_codenames:
        await event.reply(await error_message(device, locale))
        return
    message, buttons = await archive_message(device, PROVIDER.codenames_names, locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern=r'/latest(?: )?(\w+)?'))
async def latest(event):
    """Send a message when the command /latest is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        if event.message.message.endswith('/latest'):
            device = DATABASE.get_codename(event.chat_id)
        else:
            return
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in list(PROVIDER.miui_codenames):
        await event.reply(await error_message(device, locale))
        return
    message = await latest_miui_message(device, PROVIDER.miui_updates,
                                        PROVIDER.codenames_names, locale)
    await event.reply(message)
    raise events.StopPropagation
