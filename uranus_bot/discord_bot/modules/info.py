""" Info commands handler """

from uranus_bot.discord_bot.messages.info import models_message, whatis_message, codename_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.utils.error_message import error_message


@BOT.command(name='models', description='')
async def models(ctx, device):
    """Send models' numbers of a device Example: !models whyred"""
    if device not in list(PROVIDER.models_data.keys()):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await models_message(device, PROVIDER.models_data))


@BOT.command(name='whatis', description='')
async def whatis(ctx, device):
    """Send device name of a given codename Example: !whatis whyred"""
    if device not in list(PROVIDER.codenames_names.keys()):
        await ctx.send(await error_message(device))
        return
    await ctx.send(None, embed=await whatis_message(device, PROVIDER.codenames_names))


@BOT.command(name='codename', description='')
async def codename(ctx, *args):
    """Send device codename of a given device Example: !whatis mi 6"""
    device = ' '.join(args)
    embed = await codename_message(device, PROVIDER.names_codenames)
    if embed:
        await ctx.send(None, embed=embed)
