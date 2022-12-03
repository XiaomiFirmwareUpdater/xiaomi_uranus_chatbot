""" Info commands handler """

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.info import models_message, whatis_message, codename_message
from uranus_bot.messages.error_message import error_message


@BOT.hybrid_command(name='models', description='Get device models', with_app_command=True)
async def models(ctx, device):
    """Send models' numbers of a device Example: !models whyred"""
    if device not in list(BOT.provider.models_data.keys()):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await models_message(device, BOT.provider.models_data))


@BOT.hybrid_command(name='whatis', description='Get device name of a given codename', with_app_command=True)
async def whatis(ctx, device):
    """Send device name of a given codename Example: !whatis whyred"""
    if device not in list(BOT.provider.codenames_names.keys()):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await whatis_message(device, BOT.provider.codenames_names))


@BOT.command(name='codename', description='')
async def codename(ctx, *args):
    """Send device codename of a given device Example: !codename mi 6"""
    device = ' '.join(args)
    embed = await codename_message(device, BOT.provider.names_codenames)
    if embed:
        await ctx.send(None, embed=embed)
