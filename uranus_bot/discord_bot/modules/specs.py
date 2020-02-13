""" Specs command handler """

from uranus_bot.discord_bot.messages.specs import specs_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.utils.error_message import error_message


@BOT.command(name='specs')
async def specs(ctx, device):
    """Send latest specs download for a device Example: !specs whyred"""
    embed = await specs_message(device, PROVIDER.specs_data)
    if embed:
        await ctx.send(None, embed=embed)
    else:
        await ctx.send(await error_message(device))
