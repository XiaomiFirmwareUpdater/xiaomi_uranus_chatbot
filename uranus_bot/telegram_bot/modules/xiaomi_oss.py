""" OSS command handler """
from telethon import events

from uranus_bot.utils.error_message import error_message
from uranus_bot.telegram_bot.messages.xiaomi_oss import oss_message
from uranus_bot.telegram_bot.tg_bot import BOT


@BOT.on(events.NewMessage(pattern='/oss (.+)'))
async def oss(event):
    """Send a message when the command /oss is sent."""
    device = event.pattern_match.group(1)
    message = await oss_message(device)
    if message:
        await event.reply(message)
    else:
        await event.reply(await error_message(device))
    raise events.StopPropagation
