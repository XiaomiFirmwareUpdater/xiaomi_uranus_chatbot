""" TWRP command handler """

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.twrp import twrp_message
from uranus_bot.messages.error_message import error_message


@BOT.hybrid_command(name='twrp', description='Get latest TWRP recovery downloads for a device', with_app_command=True)
async def twrp(ctx, device):
    """Send latest twrp download for a device Example: !twrp whyred"""
    if device not in list(BOT.provider.twrp_data.keys()):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await twrp_message(device, BOT.provider.twrp_data))
