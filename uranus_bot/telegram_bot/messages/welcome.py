""" Welcome message generator """
from telethon import Button
from uranus_bot.telegram_bot.tg_bot import LOCALIZE, BOT_INFO


async def welcome_message(locale):
    """ Generate telegram message of welcome command """
    message = LOCALIZE.get_text(locale, "welcome")
    buttons = [
        [Button.url(LOCALIZE.get_text(locale, "join_channel"),
                    url="https://t.me/yshalsager_projects"),
         Button.url(LOCALIZE.get_text(locale, "join_group"),
                    url="https://t.me/joinchat/CRWESlKSb5yEqDwTLgWYnQ")],
        [Button.inline(LOCALIZE.get_text(locale, "read_help"), data="help"),
         Button.url(LOCALIZE.get_text(locale, "add_to_group"),
                    url="https://t.me/XiaomiGeeksBot?startgroup=true")],
        [Button.inline(LOCALIZE.get_text(locale, "bot_lang"), data="change_language"),
         Button.inline(LOCALIZE.get_text(locale, "settings_message"),
                       data="settings")]
    ]
    return message, buttons


async def welcome_in_pm_message(locale):
    """ Generate telegram message of welcome in pm """
    message = LOCALIZE.get_text(locale, "open_in_pm")
    buttons = [
        [Button.url(LOCALIZE.get_text(locale, "click_here"),
                    f"https://t.me/{BOT_INFO['username']}?start=start")]
    ]
    return message, buttons
