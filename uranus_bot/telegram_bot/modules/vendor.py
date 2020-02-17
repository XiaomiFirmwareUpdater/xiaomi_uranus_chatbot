""" vendor command handler """
from telethon import events

from uranus_bot.messages.error_message import error_message
from uranus_bot.telegram_bot.messages.vendor import vendor_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/vendor (.+)'))
async def vendor(event):
    """Send a message when the command /vendor is sent."""
    device = event.pattern_match.group(1)
    if device not in PROVIDER.vendor_codenames:
        await event.reply(await error_message(device))
        return
    message, buttons = await vendor_message(device, PROVIDER.codenames_names)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
