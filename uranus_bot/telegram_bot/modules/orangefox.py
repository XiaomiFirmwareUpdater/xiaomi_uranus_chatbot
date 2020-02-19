""" OrangeFox command handler """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.orangefox import orangefox_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/of (.+)'))
async def orangefox(event):
    """Send a message when the command /orangefox is sent."""
    device = event.pattern_match.group(1)
    locale = DATABASE.get_locale(event.chat_id)
    if device not in list(PROVIDER.orangefox_data.keys()):
        await event.reply(await error_message(device, locale))
        return
    message, buttons = await orangefox_message(device, PROVIDER.orangefox_data, locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
