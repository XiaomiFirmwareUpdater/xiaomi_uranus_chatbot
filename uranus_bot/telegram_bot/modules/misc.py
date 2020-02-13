""" Miscellaneous commands handler """
from telethon import events
from telethon.extensions import html
from uranus_bot.telegram_bot.messages.misc import arb_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/arb'))
async def arb(event):
    """Send a message when the command /arb is sent."""
    caption = await arb_message()
    await event.reply(caption, file=PROVIDER.arb, parse_mode=html)
    raise events.StopPropagation
