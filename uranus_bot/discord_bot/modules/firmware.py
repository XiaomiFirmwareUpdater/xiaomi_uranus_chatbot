""" firmware command handler """

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.firmware import firmware_message
from uranus_bot.messages.error_message import error_message


@BOT.hybrid_command(name='firmware', description='Get device firmware download page', with_app_command=True)
async def firmware(ctx, device):
    """Send firmware downloads for a device Example: !firmware whyred"""
    if device not in BOT.provider.firmware_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await firmware_message(device, BOT.provider.codenames_names))
