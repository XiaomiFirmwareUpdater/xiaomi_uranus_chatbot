""" Miscellaneous commands handler """
import io

import aiohttp
from discord import File

from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER
from uranus_bot.discord_bot.messages.misc import arb_message, unlockbl_message, \
    tools_message, guides_message


@BOT.command(name='arb')
async def arb(ctx):
    """Send Anti-Rollback Protection information and guides Example: !arb"""
    embed = await arb_message()
    await ctx.send(None, embed=embed)

    async with aiohttp.ClientSession() as session:
        async with session.get(PROVIDER.arb) as resp:
            data = io.BytesIO(await resp.read())
            await ctx.send(file=File(data, 'arb.png'))


@BOT.command(name='unlockbl')
async def unlockbl(ctx):
    """Send How to unlock the bootloader guide Example: !unlockbl"""
    embed = await unlockbl_message()
    await ctx.send(None, embed=embed)


@BOT.command(name='tools')
async def tools(ctx):
    """Send various tools for Xiaomi devices Example: !tools"""
    embed = await tools_message()
    await ctx.send(None, embed=embed)


@BOT.command(name='guides')
async def guides(ctx):
    """Send various useful guides Example: !guides"""
    embed = await guides_message()
    await ctx.send(None, embed=embed)
