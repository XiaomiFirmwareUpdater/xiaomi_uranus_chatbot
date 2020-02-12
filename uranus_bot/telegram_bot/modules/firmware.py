""" firmware command handler """
from telethon import events

from uranus_bot.utils.error_message import error_message
from uranus_bot.telegram_bot.messages.firmware import firmware_message
from uranus_bot.telegram_bot.tg_bot import BOT
from uranus_bot.telegram_bot.tg_bot import PROVIDER


@BOT.on(events.NewMessage(pattern='/firmware (.+)'))
async def firmware(event):
    """Send a message when the command /firmware is sent."""
    device = event.pattern_match.group(1)
    if device not in PROVIDER.firmware_codenames:
        await event.reply(await error_message(device))
        return
    message, buttons = await firmware_message(device, PROVIDER.codenames_names)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
