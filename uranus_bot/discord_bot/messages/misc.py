""" Miscellaneous commands handler """
from discord import Embed

from uranus_bot.providers.misc.arb import get_arb_guides


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
