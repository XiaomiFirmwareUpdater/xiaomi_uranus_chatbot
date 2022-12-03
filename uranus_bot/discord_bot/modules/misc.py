""" Miscellaneous commands handler """
import io

import aiohttp
from discord import File

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.misc import arb_message, unlockbl_message, \
    tools_message, guides_message


@BOT.hybrid_command(name='arb', description='Anti-Rollback Protection information and guides', with_app_command=True)
async def arb(ctx):
    """Send Anti-Rollback Protection information and guides Example: !arb"""
    embed = await arb_message()
    await ctx.send(None, embed=embed)

    async with aiohttp.ClientSession() as session:
        async with session.get(BOT.provider.arb) as resp:
            data = io.BytesIO(await resp.read())
            await ctx.send(file=File(data, 'arb.png'))


@BOT.hybrid_command(name='unlockbl', description='How to unlock the bootloader guide', with_app_command=True)
async def unlockbl(ctx):
    """Send How to unlock the bootloader guide Example: !unlockbl"""
    embed = await unlockbl_message()
    await ctx.send(None, embed=embed)


@BOT.hybrid_command(name='tools', description='Various tools for Xiaomi devices', with_app_command=True)
async def tools(ctx):
    """Send various tools for Xiaomi devices Example: !tools"""
    embed = await tools_message()
    await ctx.send(None, embed=embed)


@BOT.hybrid_command(name='guides', description='Various useful guides', with_app_command=True)
async def guides(ctx):
    """Send various useful guides Example: !guides"""
    embed = await guides_message()
    await ctx.send(None, embed=embed)
