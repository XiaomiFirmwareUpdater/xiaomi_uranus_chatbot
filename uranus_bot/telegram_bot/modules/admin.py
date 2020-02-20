"""Xiaomi Geeks Telegram Bot - admin module"""
from asyncio import sleep
from datetime import datetime

from telethon import events

from uranus_bot import TG_BOT_ADMINS, PARENT_DIR, TG_BOT_DB
from uranus_bot.messages.admin import stats_message
from uranus_bot.telegram_bot import DATABASE, TG_LOGGER
from uranus_bot.telegram_bot.tg_bot import BOT


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern='/stats'))
async def stats_handler(event):
    stats = DATABASE.get_stats()
    message = await stats_message(stats)
    await event.respond(message)
    raise events.StopPropagation


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern=r'/broadcast (group|channel|user) ([\s\S]*$)'))
async def broadcast_handler(event):
    chat_type = event.pattern_match.group(1)
    message = event.pattern_match.group(2)
    chats = DATABASE.get_chats(chat_type)
    for chat in chats:
        await BOT.send_message(chat[0], message)
        await sleep(2)
    raise events.StopPropagation


async def backup_database():
    """ Send database backup to bot owners daily """
    while True:
        for admin in TG_BOT_ADMINS:
            now = str(datetime.today()).split('.')[0]
            await BOT.send_message(admin, now,
                                   file=f"{PARENT_DIR}/{TG_BOT_DB}")
            TG_LOGGER.info(f"Sent database backup ({now}) to {admin}")
            await sleep(2)
        await sleep(60 * 60 * 24)


BOT.loop.create_task(backup_database())
