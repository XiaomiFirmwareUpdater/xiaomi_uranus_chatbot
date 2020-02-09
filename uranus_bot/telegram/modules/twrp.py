""" TWRP command handler """
from telethon import events

from uranus_bot.telegram.messages.twrp import twrp_message
from uranus_bot.telegram.tg_bot import BOT


@BOT.on(events.NewMessage(pattern='/twrp (.+)'))
async def twrp(event):
    """Send a message when the command /twrp is sent."""
    device = event.pattern_match.group(1)
    message, buttons = await twrp_message(device)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
