""" TWRP command handler """
from discord.ext.commands import MissingRequiredArgument
from telethon import events

from uranus_bot.discord_bot.messages.twrp import twrp_message
from uranus_bot.discord_bot.discord_bot import BOT


@BOT.command(name='twrp', description='')
async def start(ctx, device):
    """Send latest twrp download for a device Example: !twrp whyred"""
    await ctx.send(None, embed=await twrp_message(device))
