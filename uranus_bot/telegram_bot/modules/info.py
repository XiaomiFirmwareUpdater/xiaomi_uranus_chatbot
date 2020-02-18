""" info commands handlers """
from telethon import events

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.error import error_message
from uranus_bot.telegram_bot.messages.info import models_message, whatis_message, codename_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/models (.+)'))
async def models(event):
    """Send a message when the command /models is sent."""
    device = event.pattern_match.group(1).lower()
    locale = DATABASE.get_locale(event.chat_id)
    if device not in list(PROVIDER.models_data.keys()):
        await event.reply(await error_message(device, locale))
        return
    message = await models_message(device, PROVIDER.models_data, locale)
    await event.reply(message)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/whatis (.+)'))
async def whatis(event):
    """Send a message when the command /whatis is sent."""
    device = event.pattern_match.group(1).lower()
    locale = DATABASE.get_locale(event.chat_id)
    if device not in list(PROVIDER.codenames_names.keys()):
        await event.reply(await error_message(device, locale))
        return
    message = await whatis_message(device, PROVIDER.codenames_names, locale)
    await event.reply(message)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/codename (.+)'))
async def codename(event):
    """Send a message when the command /codename is sent."""
    device = event.pattern_match.group(1)
    locale = DATABASE.get_locale(event.chat_id)
    message = await codename_message(device, PROVIDER.names_codenames, locale)
    if message:
        await event.reply(message)
    raise events.StopPropagation
