#!/usr/bin/env python3.7
""" Xiaomi Geeks discord Bot"""
from importlib import import_module

from discord import ActivityType, Activity
from discord.ext import commands

from uranus_bot import DISCORD_TOKEN
from uranus_bot.discord_bot import DISCORD_LOGGER
from uranus_bot.discord_bot.modules import ALL_MODULES

BOT = commands.Bot(command_prefix='!')


@BOT.event
async def on_ready():
    """ Confirm the bot is ready """
    DISCORD_LOGGER.info("Bot started as %s! Username is %s and ID is %s",
                        BOT.user.name, BOT.user, BOT.user.id)
    activity = Activity(name='Xiaomi updates', type=ActivityType.watching)
    await BOT.change_presence(activity=activity)


# Load all modules in modules list
for module_name in ALL_MODULES:
    # print(f"{__name__.split('.')[0]}.discord_bot.modules.{module_name}")
    import_module(f"{__name__.split('.')[0]}.discord_bot.modules.{module_name}")


def main():
    """Run the bot."""
    BOT.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
