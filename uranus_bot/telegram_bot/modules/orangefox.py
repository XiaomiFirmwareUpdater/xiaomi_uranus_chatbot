""" OrangeFox command handler """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.orangefox import orangefox_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern=r'/of(?: )?(\w+)?'))
async def orangefox(event):
    """Send a message when the command /of is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        if event.message.message.endswith('/of'):
            device = DATABASE.get_codename(event.chat_id)
        else:
            return
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    try:
        message, buttons = await orangefox_message(device, locale)
        await event.reply(message, buttons=buttons, link_preview=False)
    except TypeError:
        await event.reply(await error_message(device, locale))
    raise events.StopPropagation
