""" Specs command handler """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.specs import specs_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER
from uranus_bot.telegram_bot.utils.decorators import exception_handler


@BOT.on(events.NewMessage(pattern='/specs (.+)'))
@exception_handler
async def specs(event):
    """Send a message when the command /specs is sent."""
    device = event.pattern_match.group(1)
    locale = DATABASE.get_locale(event.chat_id)
    message = await specs_message(device, PROVIDER.specs_data, locale)
    if message:
        await event.reply(message, link_preview=False)
    else:
        await event.reply(await error_message(device, locale))
    raise events.StopPropagation
