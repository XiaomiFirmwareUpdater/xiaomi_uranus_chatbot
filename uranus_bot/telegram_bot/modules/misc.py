""" Miscellaneous commands handler """
from telethon import events
from telethon.extensions import html

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.misc import arb_message, unlockbl_message,\
    tools_message, guides_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/arb'))
async def arb(event):
    """Send a message when the command /arb is sent."""
    caption = await arb_message()
    await event.reply(caption, file=PROVIDER.arb, parse_mode=html)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/unlockbl'))
async def unlockbl(event):
    """Send a message when the command /unlockbl is sent."""
    locale = DATABASE.get_locale(event.chat_id)
    message, buttons = await unlockbl_message(locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/tools'))
async def tools(event):
    """Send a message when the command /tools is sent."""
    locale = DATABASE.get_locale(event.chat_id)
    message, buttons = await tools_message(locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/guides'))
async def guides(event):
    """Send a message when the command /guides is sent."""
    locale = DATABASE.get_locale(event.chat_id)
    message, buttons = await guides_message(locale)
    await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation
