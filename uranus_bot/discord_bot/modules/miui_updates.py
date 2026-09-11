""" MIUI Updates command handler """
from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.miui_updates import (
    archive_message,
    latest_miui_message,
    miui_message,
)
from uranus_bot.messages.error_message import error_message


async def send_miui_update(ctx, device, method):
    """Send the latest recovery or fastboot ROM for a device."""
    if device not in BOT.provider.miui_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await miui_message(device, method, BOT.provider.miui_updates,
                                                  BOT.provider.codenames_names))


@BOT.hybrid_command(name='recovery', description='Get the latest recovery ROM', with_app_command=True)
async def recovery(ctx, device):
    """Send the latest recovery ROM for a device."""
    await send_miui_update(ctx, device, 'Recovery')


@BOT.hybrid_command(name='fastboot', description='Get the latest fastboot ROM', with_app_command=True)
async def fastboot(ctx, device):
    """Send the latest fastboot ROM for a device."""
    await send_miui_update(ctx, device, 'Fastboot')


@BOT.hybrid_command(name='archive', description='Get MIUI archive downloads page for a device', with_app_command=True)
async def archive(ctx, device):
    """Send MIUI archive downloads link for a device Example: !archive whyred"""
    if device not in BOT.provider.miui_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await archive_message(device, BOT.provider.codenames_names))


@BOT.hybrid_command(name='latest', description='Send latest MIUI versions for a device', with_app_command=True)
async def latest(ctx, device):
    """Send latest MIUI versions for a device Example: !latest whyred"""
    if device not in BOT.provider.miui_codenames:
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await latest_miui_message(
        device, BOT.provider.miui_updates, BOT.provider.codenames_names))
