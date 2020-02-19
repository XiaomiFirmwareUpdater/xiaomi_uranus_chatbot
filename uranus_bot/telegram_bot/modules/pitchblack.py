""" PitchBlack command handler """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.pitchblack import pitchblack_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/pb (.+)'))
async def pitchblack(event):
    """Send a message when the command /pitchblack is sent."""
    locale = DATABASE.get_locale(event.chat_id)
    device = event.pattern_match.group(1)
    if device not in str(PROVIDER.pitchblack_data):
        await event.reply(await error_message(device, locale))
        return
    message, buttons = await pitchblack_message(device, PROVIDER.pitchblack_data, locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
