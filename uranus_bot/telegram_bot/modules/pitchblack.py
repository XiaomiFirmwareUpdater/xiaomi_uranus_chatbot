""" PitchBlack command handler """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.pitchblack import pitchblack_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER
from uranus_bot.telegram_bot.utils.decorators import exception_handler


@BOT.on(events.NewMessage(pattern=r'/pb(?: )?(\w+)?'))
@exception_handler
async def pitchblack(event):
    """Send a message when the command /pb is sent."""
    try:
        device = event.pattern_match.group(1).lower()
    except (IndexError, AttributeError):
        if event.message.message.endswith('/pb'):
            device = DATABASE.get_codename(event.chat_id)
        else:
            return
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in str(PROVIDER.pitchblack_data):
        await event.reply(await error_message(device, locale))
        return
    message, buttons = await pitchblack_message(device, PROVIDER.pitchblack_data, locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
