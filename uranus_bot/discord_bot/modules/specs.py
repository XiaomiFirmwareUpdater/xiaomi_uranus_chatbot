""" Specs command handler """

from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.specs import specs_message
from uranus_bot.messages.error_message import error_message


@BOT.hybrid_command(name='specs', description='Get hardware specs for a device', with_app_command=True)
async def specs(ctx, device):
    """Get hardware specs for a device Example: !specs whyred"""
    embeds = await specs_message(device, BOT.provider.specs_data)
    if embeds:
        await ctx.send(None, embeds=embeds)
    else:
        await ctx.send(await error_message(device))
