""" Xiaomi.eu command handler """

from uranus_bot.discord_bot.messages.xiaomi_eu import eu_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.messages.error_message import error_message


@BOT.command(name='eu')
async def xiaomi_eu(ctx, device):
    """Send latest Xiaomi.eu downloads for a device Example: !eu whyred"""
    if device not in list(PROVIDER.eu_codenames.keys()):
        await ctx.send(await error_message(device))
        return
    embed = await eu_message(device, PROVIDER.eu_data, PROVIDER.eu_codenames)
    if embed:
        await ctx.send(None, embed=embed)
