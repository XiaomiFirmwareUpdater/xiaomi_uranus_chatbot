#!/usr/bin/env python3.7
""" Xiaomi Geeks Telegram Bot"""
from importlib import import_module

from telethon import TelegramClient

from uranus_bot import API_KEY, API_HASH, BOT_TOKEN, LOGGER
from uranus_bot.modules import ALL_MODULES

BOT = TelegramClient('xfu_bot', API_KEY, API_HASH).start(bot_token=BOT_TOKEN)

# Load all modules in modules list
for module_name in ALL_MODULES:
    import_module(f"{__name__.split('.')[0]}.modules.{module_name}")


def main():
    """Start the bot."""
    LOGGER.info("Bot started!")
    with BOT:
        BOT.run_until_disconnected()
