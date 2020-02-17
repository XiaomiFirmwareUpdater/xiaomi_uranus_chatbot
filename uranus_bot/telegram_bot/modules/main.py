""" Xiaomi Geeks Telegram Bot main module"""
from base64 import b64decode

from telethon import events, Button

from uranus_bot import HELP_URL
from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.modules.help import show_help
from uranus_bot.telegram_bot.modules.subscriptions import subscribe
from uranus_bot.telegram_bot.tg_bot import BOT
from uranus_bot.telegram_bot.utils.chat import get_user_info, get_chat_id


@BOT.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is sent."""
    # sender_info = await get_user_info(event)
    # DATABASE.add_chat_to_db(sender_info)
    try:
        key = event.message.message.split('/start ')[1]
    except IndexError:
        key = None
    if event.message.message.endswith('help'):
        await show_help(event)
    elif key:
        decoded = b64decode(key).decode()
        if "/subscribe" in decoded:
            event.message.message = decoded
            await subscribe(event)
    else:
        message = f"Hey! I'm Uranus, an all-in-one bot for Xiaomi users!\n" \
                  "I can get you latest Official ROMs, Firmware updates links," \
                  " and many more things!\n\nCheck how to use me by clicking help button below." \
                  "\nJoin [my channel](https://t.me/yshalsager_projects) " \
                  "to get all updates and announcements about the bot!"
        await event.reply(message, buttons=[
            [Button.url("Join my channel", url="https://t.me/yshalsager_projects"),
             Button.url("Join support group", url="https://t.me/joinchat/CRWESlKSb5yEqDwTLgWYnQ")],
            [Button.inline('Read help', data="help"),
             Button.url('Add to a group', "https://t.me/XiaomiGeeksBot?startgroup=true")]
        ], link_preview=False)
    raise events.StopPropagation  # Other handlers won't have an event to work with


# @BOT.on(events.NewMessage)
# async def echo(event):
#     """Echo the user message."""
#     await event.respond(event.text)
#     # await event.respond('A single button, with "clk1" as data',
#     #                     buttons=Button.inline('Click me', b'clk1'))


@BOT.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    """Add user to the db on new message
    This is temporary until active users are added to the database."""
    # print(event.message.text)
    if not DATABASE.is_known_chat(await get_chat_id(event)):
        DATABASE.add_chat_to_db(await get_user_info(event))


# Add new chats to database
# @BOT.on(events.chataction.ChatAction)
# async def on_adding_to_chat(event):
#     """Adds the chat that bot was added to into the database"""
#     if event.user_added and BOT_ID in event.action_message.action.users:
#         if not DATABASE.is_known_chat(await get_chat_id(event)):
#             DATABASE.add_chat_to_db(await get_user_info(event))
