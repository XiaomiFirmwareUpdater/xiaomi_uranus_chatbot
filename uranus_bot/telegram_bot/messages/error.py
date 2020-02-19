""" Error message generator """
from uranus_bot.telegram_bot.tg_bot import LOCALIZE


async def error_message(device, locale):
    """ Generate telegram message text """
    return "**Could not find" + \
           LOCALIZE.get_text(locale, 'error_message').replace(
               '{device}', device) + "**"
