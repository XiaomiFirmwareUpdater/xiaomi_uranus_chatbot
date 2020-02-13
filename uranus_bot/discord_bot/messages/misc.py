""" Miscellaneous commands handler """
from discord import Embed

from uranus_bot.providers.misc.arb import get_arb_guides
from uranus_bot.providers.misc.guides import get_guides
from uranus_bot.providers.misc.tools import get_tools
from uranus_bot.providers.misc.unlockbl import get_unlock_guides


async def arb_message():
    """ Generate discord message of arb command """
    guides = await get_arb_guides()
    message = ""
    for guide in guides:
        for title, link in guide.items():
            message += f"[{title}]({link})\n"
    embed = Embed(title=f"**Anti-Rollback Protection information and guides**",
                  description=message)
    return embed


async def unlockbl_message():
    """ Generate discord message of unlockbl command """
    guides = await get_unlock_guides()
    embed = Embed(title=f"**Unlocking bootloader guide and tool**")
    for guide in guides:
        for title, link in guide.items():
            embed.add_field(name=f'{title}', value=f'[Here]({link})')
    return embed


async def tools_message():
    """ Generate discord message of tools command """
    tools = await get_tools()
    embed = Embed(title=f"**Tools for Xiaomi devices**")
    for tool in tools:
        for title, link in tool.items():
            embed.add_field(name=f'{title}', value=f'[Here]({link})')
    return embed


async def guides_message():
    """ Generate discord message of guides command """
    guides = await get_guides()
    embed = Embed(title=f"**Guides for Xiaomi devices**")
    for guide in guides:
        for title, link in guide.items():
            embed.add_field(name=f'{title}', value=f'[Here]({link})')
    return embed
