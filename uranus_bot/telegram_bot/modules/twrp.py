""" TWRP command handler """
from telethon import events

from uranus_bot.utils.error_message import error_message
from uranus_bot.telegram_bot.messages.twrp import twrp_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/twrp (.+)'))
async def twrp(event):
    """Send a message when the command /twrp is sent."""
    device = event.pattern_match.group(1)
    if device not in list(PROVIDER.twrp_data.keys()):
        await event.reply(await error_message(device))
        return
    message, buttons = await twrp_message(device, PROVIDER.twrp_data)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
