"""Xiaomi Geeks Telegram Bot inline mode"""
import re

from telethon import events

from uranus_bot.providers.devices_info.info import get_codename
from uranus_bot.telegram_bot.messages.firmware import firmware_inline
from uranus_bot.telegram_bot.messages.info import models_inline, whatis_inline, codename_inline
from uranus_bot.telegram_bot.messages.twrp import twrp_inline
from uranus_bot.telegram_bot.messages.vendor import vendor_inline
from uranus_bot.telegram_bot.tg_bot import BOT
from uranus_bot.telegram_bot.tg_bot import PROVIDER


@BOT.on(events.InlineQuery)
async def handler(event):
    """Handle inline queries"""
    result = None
    query = None
    query_args = re.findall(r'\S+', event.text.lower().strip())
    try:
        query = query_args[0]
    except IndexError:
        pass
    try:
        query_request = query_args[1]
    except IndexError:
        query_request = None
    if query == 'twrp':
        if query_request in list(PROVIDER.twrp_data.keys()):
            result = await twrp_inline(event, query_request, PROVIDER.twrp_data)
    if query == 'firmware':
        if query_request in PROVIDER.firmware_codenames:
            result = await firmware_inline(event, query_request)
    if query == 'vendor':
        if query_request in PROVIDER.vendor_codenames:
            result = await vendor_inline(event, query_request)
    if query == 'models':
        if query_request in list(PROVIDER.models_data.keys()):
            result = await models_inline(event, query_request, PROVIDER.models_data)
    if query == 'whatis':
        if query_request in list(PROVIDER.codenames_names.keys()):
            result = await whatis_inline(event, query_request, PROVIDER.codenames_names)
    if query == 'codename':
        query_request = ' '.join(query_args[1:])
        if await get_codename(query_request, PROVIDER.names_codenames):
            result = await codename_inline(event, query_request, PROVIDER.names_codenames)
    else:
        pass
    if result:
        await event.answer([result])
