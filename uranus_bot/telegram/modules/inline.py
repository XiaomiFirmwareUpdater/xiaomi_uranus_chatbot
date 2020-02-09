"""Xiaomi Geeks Telegram Bot inline mode"""
import re

from telethon import events

from uranus_bot.telegram.messages.twrp import twrp_inline
from uranus_bot.telegram.tg_bot import BOT


@BOT.on(events.InlineQuery)
async def handler(event):
    """Handle inline queries"""
    result = None
    query_args = re.findall(r'\S+', event.text.lower().strip())
    query = query_args[0]
    try:
        query_request = query_args[1]
    except IndexError:
        query_request = None
    if query == 'twrp':
        result = await twrp_inline(event, query_request)
    else:
        pass
    if result:
        await event.answer([result])
