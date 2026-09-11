"""Discord admin command handlers."""

from discord import Embed

from uranus_bot import DISCORD_BOT_ADMINS
from uranus_bot.discord_bot import DATABASE
from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.messages.admin import stats_message


@BOT.hybrid_command(name='stats', description='Get bot usage statistics', with_app_command=True)
async def stats_handler(ctx):
    """Get bot usage statistics [Admin only]."""
    if ctx.author.id in DISCORD_BOT_ADMINS:
        stats = DATABASE.get_stats()
        message = await stats_message(stats)
        await ctx.send(None, embed=Embed(title='Stats', description=message))
