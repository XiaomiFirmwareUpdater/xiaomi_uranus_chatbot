"""Xiaomi Geeks Telegram Bot - admin module"""
from asyncio import sleep

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


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern=r'/broadcast (group|channel|user) ([\s\S]*$)'))
async def broadcast_handler(event):
    chat_type = event.pattern_match.group(1)
    message = event.pattern_match.group(2)
    chats = DATABASE.get_chats(chat_type)
    for chat in chats:
        await BOT.send_message(chat[0], message)
        await sleep(2)
    raise events.StopPropagation
