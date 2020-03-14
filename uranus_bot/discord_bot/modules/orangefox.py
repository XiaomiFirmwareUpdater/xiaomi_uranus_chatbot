""" OrangeFox command handler """

from uranus_bot.discord_bot.messages.orangefox import orangefox_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.messages.error_message import error_message


@BOT.command(name='of')
async def orangefox(ctx, device):
    """Send latest orangefox recovery downloads for a device Example: !of whyred"""
    embed = await orangefox_message(device)
    await ctx.send(None, embed=embed) if embed else await ctx.send(await error_message(device))
