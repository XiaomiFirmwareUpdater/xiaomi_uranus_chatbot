""" vendor command handler """

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.vendor import vendor_message
from uranus_bot.messages.error_message import error_message


@BOT.hybrid_command(name='vendor', description='Get vendor downloads for a device', with_app_command=True)
async def vendor(ctx, device):
    """Send vendor downloads for a device Example: !vendor whyred"""
    if device not in BOT.provider.firmware_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await vendor_message(device))
