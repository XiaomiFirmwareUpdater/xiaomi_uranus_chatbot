#!/usr/bin/env python3.7
""" Xiaomi Geeks discord Bot"""
from asyncio import run, create_task

from discord import ActivityType, Activity, Intents
from discord.ext.commands import Bot

from uranus_bot import DISCORD_TOKEN
from uranus_bot.discord_bot import DISCORD_LOGGER
from uranus_bot.discord_bot.modules import ALL_MODULES
from uranus_bot.providers.provider import Provider
from uranus_bot.utils.loader import load_modules


class MyBot(Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        intents.presences = True
        super().__init__(intents=intents, command_prefix='!')
        self.provider = None

    async def setup_hook(self):
        from uranus_bot.discord_bot.modules.subscriptions import post_miui_updates, post_firmware_updates

        self.provider = Provider(self.loop)
        # Load all modules in modules list
        load_modules(ALL_MODULES, __package__)
        # await self.tree.sync(guild=Object(id=484361541815107607))
        create_task(post_miui_updates())
        create_task(post_firmware_updates())


BOT = MyBot()


@BOT.event
async def on_ready():
    """ Confirm the bot is ready """
    DISCORD_LOGGER.info("Bot started as %s! Username is %s and ID is %s",
                        BOT.user.name, BOT.user, BOT.user.id)
    activity = Activity(name='Xiaomi updates', type=ActivityType.watching)
    await BOT.change_presence(activity=activity)


async def main():
    """Run the bot."""
    async with BOT:
        await BOT.start(DISCORD_TOKEN)


if __name__ == '__main__':
    run(main())
