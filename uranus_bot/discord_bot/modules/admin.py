""" firmware command handler """
from discord import Embed

from uranus_bot import DISCORD_BOT_ADMINS
from uranus_bot.discord_bot import DATABASE
from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.messages.admin import stats_message


@BOT.command(name='stats')
async def stats_handler(ctx):
    if ctx.author.id in DISCORD_BOT_ADMINS:
        stats = DATABASE.get_stats()
        message = await stats_message(stats)
        await ctx.send(None, embed=Embed(title="Stats", description=message))
