""" Miscellaneous messages generator """
from telethon import Button

from uranus_bot.telegram_bot.tg_bot import LOCALIZE
from uranus_bot.providers.misc.arb import get_arb_guides
from uranus_bot.providers.misc.guides import get_guides
from uranus_bot.providers.misc.tools import get_tools
from uranus_bot.providers.misc.unlockbl import get_unlock_guides


async def arb_message():
    """ Generate telegram message of arb command """
    guides = await get_arb_guides()
    message = ""
    for guide in guides:
        for title, link in guide.items():
            message += f"<a href={link}>{title}</a>\n"
    return message


async def unlockbl_message(locale):
    """ Generate telegram message of unlockbl command """
    guides = await get_unlock_guides()
    message = f"**{LOCALIZE.get_text(locale, 'unlock_bl')}**"
    buttons = []
    for guide in guides:
        for title, link in guide.items():
            buttons.append([Button.url(f"{title}", url=link)])
    return message, buttons


async def unlockbl_inline(event, locale):
    """ Generate telegram result of unlockbl inline query """
    builder = event.builder
    message, buttons = await unlockbl_message(locale)
    result = builder.article(
        LOCALIZE.get_text(locale, "unlock_bl_inline"), text=message,
        buttons=buttons, link_preview=False)
    return result


async def tools_message(locale):
    """ Generate telegram message of tools command """
    tools = await get_tools()
    message = f"**{LOCALIZE.get_text(locale, 'tools')}**"
    buttons = []
    for tool in tools:
        for title, link in tool.items():
            buttons.append([Button.url(f"{title}", url=link)])
    return message, buttons


async def tools_inline(event, locale):
    """ Generate telegram result of tools inline query """
    builder = event.builder
    message, buttons = await tools_message(locale)
    result = builder.article(
        LOCALIZE.get_text(locale, 'tools_inline'), text=message,
        buttons=buttons, link_preview=False)
    return result


async def guides_message(locale):
    """ Generate telegram message of guides command """
    guides = await get_guides()
    message = f"**{LOCALIZE.get_text(locale, 'guides')}**"
    buttons = []
    for guide in guides:
        for title, link in guide.items():
            buttons.append([Button.url(f"{title}", url=link)])
    return message, buttons


async def guides_inline(event, locale):
    """ Generate telegram result of guides inline query """
    builder = event.builder
    message, buttons = await guides_message(locale)
    result = builder.article(
        LOCALIZE.get_text(locale, 'guides_inline'), text=message,
        buttons=buttons, link_preview=False)
    return result
