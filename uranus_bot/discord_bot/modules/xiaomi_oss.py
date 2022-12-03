""" OSS command handler """

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.xiaomi_oss import oss_message
from uranus_bot.messages.error_message import error_message


@BOT.hybrid_command(name='oss', description='Get OSS kernel link for a device', with_app_command=True)
async def oss(ctx, device):
    """Get OSS kernel link for a device Example: !oss whyred"""
    embed = await oss_message(device)
    if embed:
        await ctx.send(None, embed=embed)
    else:
        await ctx.send(await error_message(device))
