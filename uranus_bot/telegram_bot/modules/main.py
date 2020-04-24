""" Xiaomi Geeks Telegram Bot main module"""
from base64 import b64decode

from telethon import events
from telethon.errors import ChatWriteForbiddenError, UserIsBlockedError

from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.welcome import welcome_message, welcome_in_pm_message
from uranus_bot.telegram_bot.modules.help import show_help
from uranus_bot.telegram_bot.modules.subscriptions import subscribe
from uranus_bot.telegram_bot.tg_bot import BOT, BOT_INFO
from uranus_bot.telegram_bot.utils.chat import get_user_info


@BOT.on(events.NewMessage(pattern=f"/start(?: )?(?:@{BOT_INFO['username']})?(?: )?(\\S+)?"))
async def start(event):
    """Send a message when the command /start is sent."""
    # sender_info = await get_user_info(event)
    # DATABASE.add_chat_to_db(sender_info)
    locale = DATABASE.get_locale(event.chat_id)
    if not event.is_private:
        message, buttons = await welcome_in_pm_message(locale)
        try:
            await event.reply(message, buttons=buttons)
        except ChatWriteForbiddenError:
            pass
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
        except UnicodeDecodeError:
            pass
    else:
        message, buttons = await welcome_message(locale)
        try:
            await event.reply(message, buttons=buttons, link_preview=False)
        except UserIsBlockedError:
            pass
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
    if not DATABASE.is_known_chat(event.chat_id):
        DATABASE.add_chat_to_db(await get_user_info(event))

# Add new chats to database
# @BOT.on(events.chataction.ChatAction)
# async def on_adding_to_chat(event):
#     """Adds the chat that bot was added to into the database"""
#     if event.user_added and BOT_ID in event.action_message.action.users:
#         if not DATABASE.is_known_chat(event.chat_id):
#             DATABASE.add_chat_to_db(await get_user_info(event))
