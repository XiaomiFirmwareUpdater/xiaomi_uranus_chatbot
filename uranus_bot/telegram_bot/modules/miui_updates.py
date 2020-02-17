""" MIUI Updates commands handlers """
from telethon import events

from uranus_bot.telegram_bot.messages.miui_updates import miui_message, \
    archive_message, latest_miui_message
from uranus_bot.messages.error_message import error_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/recovery (.+)'))
@BOT.on(events.NewMessage(pattern='/fastboot (.+)'))
async def miui(event):
    """Send a message when the command /recovery is sent."""
    device = event.pattern_match.group(1)
    if device not in list(PROVIDER.miui_codenames):
        await event.reply(await error_message(device))
        return
    updates = PROVIDER.miui_recovery_updates if "recovery" in event.pattern_match.string \
        else PROVIDER.miui_fastboot_updates
    message, buttons = await miui_message(device, updates,
                                          PROVIDER.codenames_names)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/archive (.+)'))
async def firmware(event):
    """Send a message when the command /archive is sent."""
    device = event.pattern_match.group(1)
    if device not in PROVIDER.miui_codenames:
        await event.reply(await error_message(device))
        return
    message, buttons = await archive_message(device, PROVIDER.codenames_names)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/latest (.+)'))
async def latest(event):
    """Send a message when the command /latest is sent."""
    device = event.pattern_match.group(1)
    if device not in list(PROVIDER.miui_codenames):
        await event.reply(await error_message(device))
        return
    message = await latest_miui_message(device, PROVIDER.miui_recovery_updates,
                                        PROVIDER.codenames_names)
    await event.reply(message)
    raise events.StopPropagation
