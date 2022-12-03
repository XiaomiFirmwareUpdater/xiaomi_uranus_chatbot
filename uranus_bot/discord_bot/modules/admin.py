""" firmware command handler """
from typing import Optional, Literal

from discord import Embed, Object, HTTPException
from discord.ext import commands
from discord.ext.commands import Context, Greedy

from uranus_bot import DISCORD_BOT_ADMINS
from uranus_bot.discord_bot import DATABASE
from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.messages.admin import stats_message


@BOT.command(name='stats')
async def stats_handler(ctx):
    """Get bot usage statistics [Admin only]"""
    if ctx.author.id in DISCORD_BOT_ADMINS:
        stats = DATABASE.get_stats()
        message = await stats_message(stats)
        await ctx.send(None, embed=Embed(title="Stats", description=message))


# https://discord.com/channels/336642139381301249/1043536299853881344/1043539202169647266
@BOT.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
        ctx: Context, guilds: Greedy[Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    """Sync app commands [Admin only] (' ' global, ~ current, * copy to current, ^ clear)"""
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
