""" PitchBlack command handler """

from uranus_bot.discord_bot.messages.pitchblack import pitchblack_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.messages.error_message import error_message


@BOT.command(name='pb')
async def pitchblack(ctx, device):
    """Send latest PitchBlack recovery downloads for a device Example: !pb whyred"""
    if device not in str(PROVIDER.pitchblack_data):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await pitchblack_message(device, PROVIDER.pitchblack_data))
