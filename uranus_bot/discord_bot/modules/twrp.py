""" TWRP command handler """

from uranus_bot.discord_bot.messages.twrp import twrp_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.messages.error_message import error_message


@BOT.command(name='twrp', description='')
async def twrp(ctx, device):
    """Send latest twrp download for a device Example: !twrp whyred"""
    if device not in list(PROVIDER.twrp_data.keys()):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await twrp_message(device, PROVIDER.twrp_data))
