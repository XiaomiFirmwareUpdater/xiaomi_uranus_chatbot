"""Xiaomi Geeks Telegram Bot - admin module"""
import pickle
from asyncio import sleep, create_subprocess_shell
from asyncio.subprocess import PIPE
from datetime import datetime
from os import execl
from sys import executable

from telethon import events

from uranus_bot import TG_BOT_ADMINS, PARENT_DIR, TG_BOT_DB
from uranus_bot.messages.admin import stats_message
from uranus_bot.telegram_bot import DATABASE, TG_LOGGER
from uranus_bot.telegram_bot import __package__ as main_package
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
        try:
            entity = await BOT.get_entity(chat[0])
            await BOT.send_message(entity, message)
        except ValueError:
            if chat_type == 'channel':
                entity = await BOT.get_entity(int('-100' + str(chat[0])))
                await BOT.send_message(entity, message)
            else:
                TG_LOGGER.warning("failed sending message to", chat)
        await sleep(2)
    raise events.StopPropagation


async def backup_database():
    """ Send database backup to bot owners daily """
    while True:
        now = str(datetime.today()).split('.')[0]
        await BOT.send_message(TG_BOT_ADMINS[0], now,
                               file=f"{PARENT_DIR}/{TG_BOT_DB}")
        TG_LOGGER.info(f"Sent database backup ({now}) to {TG_BOT_ADMINS[0]}")
        await sleep(60 * 60 * 24)


BOT.loop.create_task(backup_database())


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern='/update'))
async def update_handler(event):
    message = await event.respond("Updating...")
    process = await create_subprocess_shell("git pull origin master", stdin=PIPE, stdout=PIPE)
    output = await process.stdout.read()
    output = output.decode().strip()
    await process.wait()
    if output:
        await message.edit(output)
    await sleep(2)
    await message.edit("Restarting...")
    await restart(message)


@BOT.on(events.NewMessage(from_users=TG_BOT_ADMINS, pattern='/restart'))
async def restart_handler(event):
    restart_message = await event.respond("Restarting...")
    await restart(restart_message)


async def restart(restart_message):
    chat_info = {'chat': restart_message.chat_id, 'message': restart_message.id}
    with open(f"restart.pickle", "wb") as out:
        pickle.dump(chat_info, out)
    execl(executable, executable, "-m", main_package)
