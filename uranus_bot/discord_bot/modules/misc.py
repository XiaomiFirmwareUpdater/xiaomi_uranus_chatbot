""" Miscellaneous commands handler """
from discord import File
import io
import aiohttp
from uranus_bot.discord_bot.messages.misc import arb_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER


@BOT.command(name='arb')
async def arb(ctx):
    """Send Anti-Rollback Protection information and guides Example: !arb"""
    embed = await arb_message()
    await ctx.send(None, embed=embed)

    async with aiohttp.ClientSession() as session:
        async with session.get(PROVIDER.arb) as resp:
            data = io.BytesIO(await resp.read())
            await ctx.send(file=File(data, 'arb.png'))
