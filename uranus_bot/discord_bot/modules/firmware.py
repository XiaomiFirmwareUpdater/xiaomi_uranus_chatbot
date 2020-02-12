""" firmware command handler """

from uranus_bot.discord_bot.messages.firmware import firmware_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.utils.error_message import error_message


@BOT.command(name='firmware', description='')
async def firmware(ctx, device):
    """Send firmware downloads for a device Example: !firmware whyred"""
    if device not in PROVIDER.firmware_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await firmware_message(device, PROVIDER.codenames_names))
