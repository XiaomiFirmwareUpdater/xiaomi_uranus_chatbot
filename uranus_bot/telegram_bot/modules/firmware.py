""" firmware command handler """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.firmware import firmware_message
from uranus_bot.telegram_bot.tg_bot import BOT
from uranus_bot.telegram_bot.tg_bot import PROVIDER


@BOT.on(events.NewMessage(pattern=r'/firmware(?: )?(.+)?'))
async def firmware(event):
    """Send a message when the command /firmware is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        device = DATABASE.get_codename(event.chat_id)
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in PROVIDER.firmware_codenames:
        await event.reply(await error_message(device, locale))
        return
    message, buttons = await firmware_message(device, PROVIDER.codenames_names, locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
