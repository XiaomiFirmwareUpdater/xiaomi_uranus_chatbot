""" info commands handlers """
from telethon import events

from uranus_bot.messages.error_message import error_message
from uranus_bot.telegram_bot.messages.info import models_message, whatis_message, codename_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER


@BOT.on(events.NewMessage(pattern='/models (.+)'))
async def models(event):
    """Send a message when the command /models is sent."""
    device = event.pattern_match.group(1)
    if device not in list(PROVIDER.models_data.keys()):
        await event.reply(await error_message(device))
        return
    message = await models_message(device, PROVIDER.models_data)
    await event.reply(message)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/whatis (.+)'))
async def whatis(event):
    """Send a message when the command /whatis is sent."""
    device = event.pattern_match.group(1)
    if device not in list(PROVIDER.codenames_names.keys()):
        await event.reply(await error_message(device))
        return
    message = await whatis_message(device, PROVIDER.codenames_names)
    await event.reply(message)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern='/codename (.+)'))
async def codename(event):
    """Send a message when the command /codename is sent."""
    device = event.pattern_match.group(1)
    message = await codename_message(device, PROVIDER.names_codenames)
    if message:
        await event.reply(message)
    raise events.StopPropagation
