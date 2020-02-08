""" Xiaomi Geeks Telegram Bot main module"""
from telethon import events, Button

from uranus_bot import DATABASE, HELP_URL, BOT_ID
from uranus_bot.tg_bot import BOT
from uranus_bot.utils.chat import get_user_info


@BOT.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is sent."""
    sender_info = await get_user_info(event)
    # DATABASE.add_chat_to_db(sender_info)
    message = f"Hello {sender_info['name']}!\n" \
              "I'm Uranus, an all-in-one bot for Xiaomi users!\n" \
              "I can get you latest Official ROMs, Firmware updates links," \
              " and many more things!\n\nCheck how to use me by clicking help button below." \
              "\nJoin [my channel](https://t.me/yshalsager_projects) " \
              "to get all updates and announcements about the bot!"
    await event.respond(message, buttons=[
        [Button.url("Join my channel", url="https://t.me/yshalsager_projects"),
         Button.url("Join support group", url="https://t.me/joinchat/CRWESlKSb5yEqDwTLgWYnQ")],
        [Button.url('Read help', HELP_URL)]
    ], link_preview=False)
    # await event.reply('Hi!')
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
    sender_info = await get_user_info(event)
    DATABASE.add_chat_to_db(sender_info)


@BOT.on(events.chataction.ChatAction)
async def on_adding_to_chat(event):
    """Adds the chat that bot was added to into the database"""
    if event.user_added and BOT_ID in event.action_message.action.users:
        sender_info = await get_user_info(event)
        DATABASE.add_chat_to_db(sender_info)
