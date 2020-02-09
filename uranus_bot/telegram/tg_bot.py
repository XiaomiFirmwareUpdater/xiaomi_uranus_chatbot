#!/usr/bin/env python3.7
""" Xiaomi Geeks Telegram Bot"""
import asyncio
from importlib import import_module

from telethon.sync import TelegramClient

from uranus_bot import API_KEY, API_HASH, BOT_TOKEN, LOGGER
from uranus_bot.telegram.modules import ALL_MODULES

BOT = TelegramClient('xfu_bot', API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
BOT.parse_mode = 'markdown'
BOT_INFO = {}


def main():
    """Main"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


async def run():
    """Run the bot."""
    bot_info = await BOT.get_me()
    BOT_INFO.update({'name': bot_info.first_name,
                     'username': bot_info.username, 'id': bot_info.id})
    LOGGER.info("Bot started as %s! Username is %s and ID is %s",
                BOT_INFO['name'], BOT_INFO['username'], BOT_INFO['id'])
    # Load all modules in modules list
    for module_name in ALL_MODULES:
        # print(f"{__name__.split('.')[0]}.telegram.modules.{module_name}")
        import_module(f"{__name__.split('.')[0]}.telegram.modules.{module_name}")
    async with BOT:
        await BOT.run_until_disconnected()
