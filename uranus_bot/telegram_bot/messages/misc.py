""" Miscellaneous messages generator """

from uranus_bot.providers.misc.arb import get_arb_guides


async def arb_message():
    """ Generate telegram message of arb command """
    guides = await get_arb_guides()
    message = ""
    for guide in guides:
        for title, link in guide.items():
            message += f"<a href={link}>{title}</a>\n"
    return message
