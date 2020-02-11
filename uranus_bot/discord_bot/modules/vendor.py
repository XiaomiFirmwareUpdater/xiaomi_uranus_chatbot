""" vendor command handler """

from uranus_bot.discord_bot.messages.vendor import vendor_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.utils.error_message import error_message


@BOT.command(name='vendor', description='')
async def vendor(ctx, device):
    """Send vendor downloads for a device Example: !vendor whyred"""
    if device not in PROVIDER.firmware_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await vendor_message(device))
