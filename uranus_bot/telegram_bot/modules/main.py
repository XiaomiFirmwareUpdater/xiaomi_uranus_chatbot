""" Xiaomi Geeks Telegram Bot main module"""
from base64 import b64decode
from binascii import Error

from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.welcome import welcome_message, welcome_in_pm_message
from uranus_bot.telegram_bot.modules.help import show_help
from uranus_bot.telegram_bot.modules.subscriptions import subscribe
from uranus_bot.telegram_bot.tg_bot import BOT, BOT_INFO
from uranus_bot.telegram_bot.utils.chat import get_user_info
from uranus_bot.telegram_bot.utils.decorators import exception_handler


@BOT.on(events.NewMessage(pattern=r"/start(?: )?(@{})?(?:\s+)?".format(BOT_INFO['username'])))
@exception_handler
async def start(event):
    """Send a message when the command /start is sent."""
    if not DATABASE.is_known_chat(event.chat_id):
        sender_info = await get_user_info(event)
        DATABASE.add_chat_to_db(sender_info)
    locale = DATABASE.get_locale(event.chat_id)
    if event.is_group:
        if event.pattern_match.group(1) or list(
                filter(lambda x: x.id == BOT_INFO['id'] or event.message.sender_id == x.id,
                       await event.client.get_participants(
                           event.chat_id, filter=ChannelParticipantsAdmins))):
            message, buttons = await welcome_in_pm_message(locale)
            await event.reply(message, buttons=buttons)
            return
    try:
        key = event.message.message.split('/start ')[1]
    except IndexError:
        key = None
    if event.message.message.endswith('help'):
        await show_help(event)
    elif key and key != 'start':
        try:
            decoded = b64decode(key).decode()
            if "/subscribe" in decoded:
                event.message.message = decoded
                await subscribe(event)
        except (UnicodeDecodeError, Error, ValueError):
            pass
    elif event.is_private:
        message, buttons = await welcome_message(locale)
        await event.reply(message, buttons=buttons, link_preview=False)
    raise events.StopPropagation  # Other handlers won't have an event to work with


# @BOT.on(events.NewMessage)
# async def echo(event):
#     """Echo the user message."""
#     await event.respond(event.text)
#     # await event.respond('A single button, with "clk1" as data',
#     #                     buttons=Button.inline('Click me', b'clk1'))


# @BOT.on(events.NewMessage(incoming=True))
# async def on_new_message(event):
#     """Add user to the db on new message
#     This is temporary until active users are added to the database."""
#     # print(event.message.text)
#     if not DATABASE.is_known_chat(event.chat_id):
#         DATABASE.add_chat_to_db(await get_user_info(event))

# Add new chats to database
@BOT.on(events.chataction.ChatAction)
async def on_adding_to_chat(event):
    """Adds the chat that bot was added to into the database"""
    if event.user_added and BOT_INFO['id'] == event.user_id:
        if not DATABASE.is_known_chat(event.chat_id):
            DATABASE.add_chat_to_db(await get_user_info(event))
