""" Specs command handler """
from telethon import events

from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.specs import specs_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/specs (.+)'))
async def specs(event):
    """Send a message when the command /specs is sent."""
    device = event.pattern_match.group(1)
    message = await specs_message(device, PROVIDER.specs_data)
    if message:
        await event.reply(message)
    else:
        await event.reply(await error_message(device, 'en'))
    raise events.StopPropagation
