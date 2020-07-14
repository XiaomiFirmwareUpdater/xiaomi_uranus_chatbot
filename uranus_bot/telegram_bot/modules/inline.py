"""Xiaomi Geeks Telegram Bot inline mode"""
import re

from telethon import events

from uranus_bot.providers.devices_info.info import get_codename
from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.firmware import firmware_inline
from uranus_bot.telegram_bot.messages.info import models_inline, whatis_inline, codename_inline
from uranus_bot.telegram_bot.messages.misc import unlockbl_inline, tools_inline, guides_inline
from uranus_bot.telegram_bot.messages.miui_updates import miui_inline, \
    archive_inline, latest_miui_inline
from uranus_bot.telegram_bot.messages.orangefox import orangefox_inline
from uranus_bot.telegram_bot.messages.pitchblack import pitchblack_inline
from uranus_bot.telegram_bot.messages.specs import specs_inline
from uranus_bot.telegram_bot.messages.twrp import twrp_inline
from uranus_bot.telegram_bot.messages.vendor import vendor_inline
from uranus_bot.telegram_bot.messages.xiaomi_eu import eu_inline
from uranus_bot.telegram_bot.messages.xiaomi_oss import oss_inline
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.InlineQuery)
async def handler(event):
    """Handle inline queries"""
    # pylint: disable=too-many-branches, too-many-statements
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
    locale = DATABASE.get_locale(event.chat_id)
    if query == 'twrp' and query_request is not None:
        if query_request in list(PROVIDER.twrp_data.keys()):
            result = await twrp_inline(event, query_request, PROVIDER.twrp_data, locale)
    if query == 'of' and query_request is not None:
        result = await orangefox_inline(event, query_request, locale)
    if query == 'pb' and query_request is not None:
        if query_request in str(PROVIDER.pitchblack_data):
            result = await pitchblack_inline(event, query_request, PROVIDER.pitchblack_data, locale)
    if query == 'firmware' and query_request is not None:
        if query_request in PROVIDER.firmware_codenames:
            result = await firmware_inline(event, query_request, PROVIDER.codenames_names, locale)
    if query == 'vendor' and query_request is not None:
        if query_request in PROVIDER.vendor_codenames:
            result = await vendor_inline(event, query_request, PROVIDER.codenames_names, locale)
    if query == 'models' and query_request is not None:
        if query_request in list(PROVIDER.models_data.keys()):
            result = await models_inline(event, query_request, PROVIDER.models_data, locale)
    if query == 'whatis' and query_request is not None:
        if query_request in list(PROVIDER.codenames_names.keys()):
            result = await whatis_inline(event, query_request, PROVIDER.codenames_names, locale)
    if query == 'codename':
        query_request = ' '.join(query_args[1:])
        if await get_codename(query_request, PROVIDER.names_codenames):
            result = await codename_inline(event, query_request, PROVIDER.names_codenames, locale)
    if query == 'recovery' and query_request is not None:
        if query_request in list(PROVIDER.miui_codenames):
            result = await miui_inline(event, query_request, "Recovery", PROVIDER.miui_updates,
                                       PROVIDER.codenames_names, locale)
    if query == 'fastboot' and query_request is not None:
        if query_request in list(PROVIDER.miui_codenames):
            result = await miui_inline(event, query_request, "Fastboot", PROVIDER.miui_updates,
                                       PROVIDER.codenames_names, locale)
    if query == 'latest' and query_request is not None:
        if query_request in list(PROVIDER.miui_codenames):
            result = await latest_miui_inline(event, query_request, PROVIDER.miui_updates,
                                              PROVIDER.codenames_names, locale)
    if query == 'archive' and query_request is not None:
        if query_request in PROVIDER.miui_codenames:
            result = await archive_inline(event, query_request, PROVIDER.codenames_names, locale)
    if query == 'eu' and query_request is not None:
        if query_request in list(PROVIDER.eu_codenames.keys()):
            result = await eu_inline(event, query_request, PROVIDER.eu_data, PROVIDER.eu_codenames, locale)
    if query == 'specs' and query_request is not None:
        result = await specs_inline(event, query_request, PROVIDER.specs_data, locale)
    if query == 'oss' and query_request is not None:
        result = await oss_inline(event, query_request, locale)
    if query == 'unlockbl':
        result = await unlockbl_inline(event, locale)
    if query == 'tools':
        result = await tools_inline(event, locale)
    if query == 'guides':
        result = await guides_inline(event, locale)
    else:
        pass
    if result:
        await event.answer([result])
