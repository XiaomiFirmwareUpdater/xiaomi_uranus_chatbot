""" TWRP command handler """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.twrp import twrp_message
from uranus_bot.telegram_bot.tg_bot import BOT, BOT_INFO, PROVIDER
from uranus_bot.telegram_bot.utils.decorators import exception_handler


@BOT.on(
    events.NewMessage(
        pattern=r"^^/twrp(?: (?P<codename>[^@]\w+)|@{} ?(?P<codename2>\w+)?)?".format(
            BOT_INFO["username"]
        )
    )
)
@exception_handler
async def twrp(event):
    """Send a message when the command /twrp is sent."""
    try:
        device = event.pattern_match.groupdict()[event.pattern_match.lastgroup]
    except (IndexError, AttributeError, KeyError):
        if event.message.message.endswith("/twrp"):
            device = DATABASE.get_codename(event.chat_id)
        else:
            return
    if not device:
        return
    locale = DATABASE.get_locale(event.chat_id)
    if device not in list(PROVIDER.twrp_data.keys()):
        await event.reply(await error_message(device, locale))
        return
    message, buttons = await twrp_message(device, PROVIDER.twrp_data, locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
