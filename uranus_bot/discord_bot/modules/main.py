""" Xiaomi Geeks Discord Bot main module"""

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.main import start_message


@BOT.command(name='start')
async def start(ctx):
    """Sends the welcome message"""
    await ctx.send(None, embed=await start_message())


@BOT.event
async def on_message(message):
    """Deal with incoming messages"""
    # Greet first time users
    if not message.guild and message.author != BOT.user and not message.channel.history(limit=1):
        await message.channel.send(None, embed=await start_message())
    else:
        await BOT.process_commands(message)
    # elif not message.guild and message.author != BOT.user:
    #     await message.channel.send("I didn't get that! Please read usage using `!help` command.")
