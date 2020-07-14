""" MIUI Updates command handler """
from uranus_bot.discord_bot.messages.miui_updates import miui_message, \
    archive_message, latest_miui_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.messages.error_message import error_message


@BOT.command(name='recovery', aliases=['fastboot'])
async def miui_updates(ctx, device):
    """Send latest recovery/fastboot ROMs
    for a device Example: !recovery whyred / !fastboot whyred"""
    if device not in PROVIDER.miui_codenames:
        await ctx.send(await error_message(device))
        return
    method = "Recovery" if ctx.invoked_with == "recovery" else "Fastboot"
    await ctx.send(None, embed=await miui_message(device, method, PROVIDER.miui_updates,
                                                  PROVIDER.codenames_names))


@BOT.command(name='archive')
async def archive(ctx, device):
    """Send MIUI archive downloads link for a device Example: !archive whyred"""
    if device not in PROVIDER.miui_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await archive_message(device, PROVIDER.codenames_names))


@BOT.command(name='latest')
async def latest(ctx, device):
    """Send latest MIUI versions for a device Example: !latest whyred"""
    if device not in PROVIDER.miui_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await latest_miui_message(
        device, PROVIDER.miui_updates, PROVIDER.codenames_names))
