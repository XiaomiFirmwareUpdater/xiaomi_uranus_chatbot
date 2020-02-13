""" OrangeFox command handler """
from telethon import events

from uranus_bot.utils.error_message import error_message
from uranus_bot.telegram_bot.messages.orangefox import orangefox_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/of (.+)'))
async def orangefox(event):
    """Send a message when the command /orangefox is sent."""
    device = event.pattern_match.group(1)
    if device not in list(PROVIDER.orangefox_data.keys()):
        await event.reply(await error_message(device))
        return
    message, buttons = await orangefox_message(device, PROVIDER.orangefox_data)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
