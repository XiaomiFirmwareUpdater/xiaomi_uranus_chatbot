""" OrangeFox command handler """

from uranus_bot.discord_bot.messages.orangefox import orangefox_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.utils.error_message import error_message


@BOT.command(name='of')
async def orangefox(ctx, device):
    """Send latest orangefox recovery downloads for a device Example: !of whyred"""
    if device not in list(PROVIDER.orangefox_data.keys()):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await orangefox_message(device, PROVIDER.orangefox_data))
