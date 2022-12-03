""" PitchBlack command handler """

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.pitchblack import pitchblack_message
from uranus_bot.messages.error_message import error_message


@BOT.hybrid_command(name='pb', description='Get latest PitchBlack recovery downloads for a device',
                    with_app_command=True)
async def pitchblack(ctx, device):
    """Send latest PitchBlack recovery downloads for a device Example: !pb whyred"""
    if device not in str(BOT.provider.pitchblack_data):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await pitchblack_message(device, BOT.provider.pitchblack_data))
