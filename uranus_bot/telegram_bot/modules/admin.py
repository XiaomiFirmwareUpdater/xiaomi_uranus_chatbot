"""Xiaomi Geeks Telegram Bot - admin module"""

from telethon import events

from uranus_bot import TG_BOT_ADMINS
from uranus_bot.messages.admin import stats_message
from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.tg_bot import BOT


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern='/stats'))
async def stats_handler(event):
    stats = DATABASE.get_stats()
    message = await stats_message(stats)
    await event.respond(message)
    raise events.StopPropagation
